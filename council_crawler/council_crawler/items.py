# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Event(scrapy.Item):

    # Required
    _type = scrapy.Field()
    name = scrapy.Field()
    scraped_datetime = scrapy.Field()
    source_url = scrapy.Field()
    source = scrapy.Field()

    # Optional - add if available
    record_date = scrapy.Field()
    documents = scrapy.Field() # List of document dicts
    meeting_type = scrapy.Field()
