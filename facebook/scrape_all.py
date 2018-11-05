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
suppliers = database.get_community_suppliers()
cookies_to_use = cookies.get_facebook_cookie("idof@live.com.au", "q1as1z2qwe2")

print(cookies_to_use)

for supplier in suppliers[10: 20]:

    supplier_id = supplier[0]

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    })

    process.crawl(comment_spider, supplier[1], supplier[2], user_id, cookies_to_use , supplier_id)

process.start()