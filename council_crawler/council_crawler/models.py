import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, String, Integer, Date, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from council_crawler import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Connect using STORAGE_ENGINE from settings.py
    Returns sqlalchemy engine
    """
    return create_engine(settings.STORAGE_ENGINE)


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class Place(DeclarativeBase):
    """Place table"""
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    place = Column(String)
    type_ = Column(String)
    state = Column(String)
    country = Column(String)
    display_name = Column(String)
    ocd_division_id = Column(String, index=True)
    seed_url = Column(String)
    hosting_service = Column(String)
    crawler = Column(Boolean, default=False)
    craler_name = Column(String)
    crawler_type = Column(String)
    crawler_owner = Column(String)


class UrlStage(DeclarativeBase):
    """Url Staging Table"""
    __tablename__ = 'url_stage'

    id = Column(Integer, primary_key=True)
    ocd_division_id = Column(String)
    event = Column(String)
    event_date = Column(Date)
    url = Column(String)
    url_hash = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)


class EventStage(DeclarativeBase):
    """Event table"""
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    ocd_division_id = Column(String)
    # place_id = Column('place_id', Integer, ForeignKey('place.id'),
    #                   nullable=False, index=True)
    name = Column(String)
    scraped_datetime = Column(DateTime, default=datetime.datetime.now)
    record_date = Column(Date)
    source = Column(String)
    source_url = Column(String)
    meeting_type = Column(String)


if __name__ == '__main__':
    engine = db_connect()
    create_tables(engine)
