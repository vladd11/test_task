BOT_NAME = "alco"

SPIDER_MODULES = ["alco.spiders"]
NEWSPIDER_MODULE = "alco.spiders"

ADDONS = {}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36 Edg/142.0.0.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 5
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429]

DUPEFILTER_CLASS = 'alco.custom_filters.URLDupeFilter'
DEFAULT_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "Cache-control": "no-cache",
    "Pragma": "no-cache",
    "Priority": "u=1, i",
    "Sec-ch-ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "Sec-ch-ua-mobile": "?1",
    "Sec-ch-ua-platform": "\"Android\"",
    "Sec-fetch-dest": "empty",
    "Sec-fetch-mode": "cors",
    "Sec-fetch-site": "same-origin",
    "Cookie": "alkoteka_locality=%7B%22uuid%22%3A%224a70f9e0-46ae-11e7-83ff-00155d026416%22%2C%22name%22%3A%22%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%22%2C%22slug%22%3A%22krasnodar%22%2C%22longitude%22%3A%2238.975996%22%2C%22latitude%22%3A%2245.040216%22%2C%22accented%22%3Atrue%7D; alkoteka_geo=true; alkoteka_cookies=true; alkoteka_age_confirm=true; XSRF-TOKEN=eyJpdiI6InZTVnZvV2Z0ei85MVNlajhFVmNwM3c9PSIsInZhbHVlIjoiN0cvcEcrb21JZWEvS3hKVEVkR0RnNmp5KzBXb0tJMW9zTlUveE4vY0RZU3MzNHYzRGNDTnB3UXIvL25iZ0J1dzFPRjFibWJ3R2pITWxiZERWR0I1eS9TSUE2dld0RjN1QmNucU1ZT3Bpakt6amx6NEo4Y2hJbURGWURsNnRJWWsiLCJtYWMiOiIxMTMxYjUwZDVkMjRjNGQzYWE3OTI0ZDFjNDdjZjYwNGQ0MzQzNWM2ZjE4MDUwYTY5ZjM2NGI4ZWYzZWY3YTE3IiwidGFnIjoiIn0%3D; sid=eyJpdiI6Ik14QWlRMm83ZWJ1b1IyeTcyMWV5Q0E9PSIsInZhbHVlIjoiYzFQZlVITXFIa0U5eVRmazRWUnZobXJaUjhYU1JiU0hLK1RNZVArK1pQNlRQU0ZBa0lRL3lhTmlRS3B6WDd0N09wK2VNL3hJcUJSY0d4ZCtBNG1iTFVjS1VCTWhlNlFVVTBKdjVKVVdGR0w5Z2lWMWtvZm9BaXpVYUpzK1lUcDIiLCJtYWMiOiI2Y2U4NWEzN2M4ZmZhYmE1MDdiODhjNjFkMThlN2NmNDYwMjE0MzQ5NGIyMjkzMzRmNmI2MWE3ZTE1Yjg1MGZkIiwidGFnIjoiIn0%3D",
    "Referer": "https://alkoteka.com/product/vermut-1/chinzano-rosso_51736"
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'alco.middlewares.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "alco.pipelines.DuplicatesPipeline": 300,
}

PROXY_LIST = 'proxies.txt'
PROXY_MODE = 0

FEED_EXPORT_ENCODING = "utf-8"
