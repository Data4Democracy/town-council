# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from council_crawler.items import Link
import sqlite3


def save_url(item):
    connection = sqlite3.connect('./scrapedata.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS myscrapedata ' \
                '(id INTEGER PRIMARY KEY, url VARCHAR(80), desc VARCHAR(80))')
    print(item['url'])
    cursor.execute(
        "insert into myscrapedata (url) values (?)",
            (item['url'],))
    connection.commit()
    return item


class CouncilCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Link):
            save_url(item)
        return item
