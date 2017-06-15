import datetime

from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

from council_crawler.items import Event
from council_crawler import models


class ValidateOCDIDPipeline(object):
    """Validate OCD ID"""
    def process_item(self, event, spider):
        ocd_id = event.get('ocd_division_id')
        if isinstance(ocd_id, str):
            # TODO add more validation on formating
            if ocd_id.startswith('ocd-'):
                return event
        else:
            raise DropItem("ocd_division_id is invalid")


class ValidateRecordDatePipeline(object):
    """Validate record_date is valid date time"""
    def process_item(self, event, spider):
        record_date = event['record_date']
        if isinstance(record_date, datetime.date):
            return event
        else:
            raise DropItem(f"{record_date} is not valid datetime object")


class CreateEventPipeline(object):
    """Store events in staging table"""
    def __init__(self):
        engine = models.db_connect()
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
    """Store links to media"""
    def __init__(self):
        engine = models.db_connect()
        models.create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, event, spider):
        if isinstance(event, Event):
            session = self.Session()

            # Save each document link attached to event
            for doc in event['documents']:
                doc_record = models.UrlStage(
                    ocd_division_id=event['ocd_division_id'],
                    event=event['name'],
                    event_date=event['record_date'],
                    url=doc['url'],
                    url_hash=doc['url_hash'],
                    category=doc['category'],
                )

                try:
                    session.add(doc_record)
                    session.commit()
                except:
                    raise
                finally:
                    session.close()
        return event

