import json
import traceback
from datetime import datetime
from typing import Any, Mapping, List
from urllib.parse import urlparse, quote_plus

import scrapy

from alco.items import Product, PriceData, AssetsData, StockData


class AlcoSpider(scrapy.Spider):
    START_URLS = [
        "https://alkoteka.com/catalog/bezalkogolnye-napitki-1/options-categories_voda",
    ]
    name = "alco_spider"
    API_URL = "https://alkoteka.com/web-api/v1"
    CATALOG_URL = "https://alkoteka.com/catalog/"
    CITY_UUID = "4a70f9e0-46ae-11e7-83ff-00155d026416"

    # Если ставить очень большой лимит, то такие запросы очень быстро забанят
    PAGE_LIMIT = 20

    def build_options(self, options: List[str]) -> str:
        if len(options) == 0:
            return ''

        def generate_options():
            for o in options:
                if o.startswith("options-categories"):
                    key, value = o.split('_', 1)
                    yield f'{quote_plus(f'options[{key[8:]}][]')}={quote_plus(value)}'

        return '&' + '&'.join(generate_options())

    def build_url(self, category: str, options: List[str], page: int) -> str:
        return f"{self.API_URL}/product?city_uuid={self.CITY_UUID}&page={page}&per_page={self.PAGE_LIMIT}&root_category_slug={category}{self.build_options(options)}"

    def parse_url(self, url: str) -> tuple[str, list[str]]:
        path = urlparse(url).path.rstrip('/').split('/')
        return path[2], path[3:]

    async def start(self):
        # Не можем использовать стандартный start, так как все сайт использует Client-side rendering
        # Все данные запрашиваем с их API
        for url in self.START_URLS:
            try:
                category, options = self.parse_url(url)
                yield scrapy.Request(url=self.build_url(category, options, 1), callback=self.parse,
                                     cb_kwargs={'category': category, 'options': options})
            except Exception:
                print(f'Can\'t request {url}')
                traceback.print_exc()

    def parse(self, response, **kwargs: Any):
        data = json.loads(response.text)

        yield from self.parse_pages(response)
        for i in range(2, -(data['meta']['total'] // -data['meta']['per_page'])):
            yield scrapy.Request(url=self.build_url(kwargs['category'], kwargs['options'], i),
                                 callback=self.parse_pages)

    # Под results нет смысла делать датакласс, так как он зависит от сайта и (может) часто меняться
    # В таком случае, если какой-то из field пропадёт или появиться новый, то парсер просто крашнется
    def convert_to_canon(self, result: Mapping[str, Any], url: str, action_labels: List[Mapping[str, Any]]):
        brand = ''
        for block in result.get('description_blocks', []):
            if block.get('code') == 'brend':
                for val in block.get('values', []):
                    if val['enabled']:
                        brand = val['name']

        description = ' '.join(block.get('content', '') for block in result['text_blocks'])
        metadata = {
            '__description': description
        }

        for block in result.get('description_blocks', []):
            for val in block.get('values', []):
                if val.get('enabled'):
                    metadata[block['code']] = val['name']

        def parse_category(category: Mapping[str, Any]):
            while category:
                yield category['name']
                category = category.get('parent')

        return Product(timestamp=int(datetime.now().timestamp() * 1e3),
                       RPC=result['uuid'],
                       url=url,
                       title=result['name'],
                       marketing_tags=[item['title'] for item in action_labels],
                       brand=brand,
                       # Здесь subname = бренд, но он указан не на всех товарах
                       section=list(parse_category(result.get('category'))),
                       price_data=PriceData(
                           original=result.get('prev_price') or result['price'],
                           current=result['price']
                       ),
                       metadata=metadata,
                       variants=1,
                       stock=StockData(
                           in_stock=result['available'],
                           count=result['quantity_total']
                       ),
                       assets=AssetsData(
                           main_image=result.get('image_url'),
                           view360=[],
                           set_images=[result.get('image_url')],
                           video=[]
                       ))

    def parse_pages(self, response: scrapy.http.Response, **kwargs: Any):
        data = json.loads(response.text)

        for result in data['results']:
            if result['available']:
                yield scrapy.Request(
                    url=f'https://alkoteka.com/web-api/v1/product/{result["slug"]}?city_uuid={self.CITY_UUID}',
                    callback=self.parse_product,
                    cb_kwargs={'url': result['product_url'], 'action_labels': result['action_labels']})

    def parse_product(self, response: scrapy.http.Response, url: str, action_labels: List[Mapping[str, Any]],
                      **kwargs: Any):
        data = json.loads(response.text)
        yield self.convert_to_canon(data['results'], url, action_labels)
