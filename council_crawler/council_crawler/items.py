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


class Event(scrapy.Item):

    # http://docs.opencivicdata.org/en/latest/data/event.html
    _type = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    start_time = scrapy.Field()
    timezone = scrapy.Field()
    end_time = scrapy.Field()
    all_day = scrapy.Field()
    status = scrapy.Field()
    source = scrapy.Field()


class Link(scrapy.Item):
    event = scrapy.Field()  # link to event entity
    media_type = scrapy.Field()
    url = scrapy.Field()
    url_hash = scrapy.Field()
    text = scrapy.Field()

    # updated
    # created
