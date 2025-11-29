# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from alco.items import Product


class DuplicatesPipeline:
    ids = set()

    def process_item(self, item: Product, spider):
        if item.RPC in self.ids:
            raise DropItem
        self.ids.add(item.RPC)
        return item
