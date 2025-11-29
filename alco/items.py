# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import dataclasses
from dataclasses import dataclass
from typing import List, Mapping


@dataclass
class PriceData:
    current: float
    original: float
    sale_tag: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.sale_tag = f'Скидка {round(self.original / self.current * 100) - 100}%'


@dataclass
class StockData:
    in_stock: bool
    count: int


@dataclass
class AssetsData:
    main_image: str
    set_images: List[str]
    view360: List[str]
    video: List[str]


@dataclass
class Product:
    timestamp: int
    RPC: str
    url: str
    title: str
    marketing_tags: List[str]
    brand: str
    section: List[str]
    price_data: PriceData
    stock: StockData
    assets: AssetsData
    metadata: Mapping[str, str]
    variants: int

