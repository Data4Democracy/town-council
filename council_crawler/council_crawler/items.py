# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Record(scrapy.Item):

    # Required
    scraped_datetime = scrapy.Field()
    record_date = scrapy.Field()
    source_url = scrapy.Field()
    source = scrapy.Field()

    # Additional info
    meeting_type = scrapy.Field()
    agenda_url = scrapy.Field()
    video_url = scrapy.Field()
    minutes_url = scrapy.Field()
