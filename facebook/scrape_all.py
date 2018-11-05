import sys
import scrapy
import time
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.crawler import CrawlerProcess
from facebook import db
from facebook.help import cookies, url

settings = project.get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
comment_spider = spider_loader.load("comments")

user_id = 100001142520539

database = db.db()
suppliers = database.get_suppliers()
cookies_to_use = cookies.get_facebook_cookie("idof@live.com.au", "q1as1z2qwe2")

for supplier in suppliers:
    supplier_id = supplier[0]

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(comment_spider, supplier[2], user_id, cookies_to_use , supplier_id)

process.start()