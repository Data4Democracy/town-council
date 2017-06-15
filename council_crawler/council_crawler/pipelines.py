import datetime

from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

from council_crawler.items import Event
from council_crawler.db_utils import stage_url, get_or_create_event
from council_crawler import models


class ValidateRecordDatePipeline(object):
    """Validate record_date is valid date time"""
    def process_item(self, item, spider):
        record_date = item['record_date']
        if isinstance(record_date, datetime.date):
            return item
        else:
            raise DropItem(f"{record_date} is not valid datetime object")


class CreateEventPipeline(object):
    def __init__(self):
        engine = models.db_connect()
        print('-------INIT INIT INIT---------')
        models.create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, event, spider):
        if isinstance(event, Event):
            session = self.Session()

            event_record = models.EventStage(
                ocd_division_id = event['ocd_division_id'],
                name=event['name'],
                scraped_datetime=event['scraped_datetime'],
                record_date=event['record_date'],
                source=event['source'],
                source_url=event['source_url'],
                meeting_type=event['meeting_type']
                )

            try:
                session.add(event_record)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        return event


class StageDocumentLinkPipeline(object):
    """Stores links to media"""
    def process_item(self, item, spider):
        if isinstance(item, Event):
            for doc in item['documents']:
                stage_url(doc, item)
        return item

