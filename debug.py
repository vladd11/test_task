from scrapy import cmdline
cmdline.execute("scrapy crawl alco_spider -O result.json".split())
