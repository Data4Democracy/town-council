import datetime

from scrapy.exceptions import DropItem

from council_crawler.items import Event
from council_crawler.db_utils import stage_url, get_or_create_event


class ValidateRecordDatePipeline(object):
    def process_item(self, item, spider):
        record_date = item['record_date']
        if isinstance(record_date, datetime.date):
            return item
        else:
            raise DropItem(f"{record_date} is not valid datetime object")


class CreateEventPipeline(object):
    """Creates event"""
    def process_item(self, item, spider):
        if isinstance(item, Event):
            get_or_create_event(item)
        return item


class StageDocumentLinkPipeline(object):
    """Stores links to media"""
    def process_item(self, item, spider):
        if isinstance(item, Event):
            for doc in item['documents']:
                stage_url(doc, item)
        return item
