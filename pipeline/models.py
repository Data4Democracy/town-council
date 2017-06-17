import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, String, Integer, Date, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Index

DeclarativeBase = declarative_base()


def db_connect():
    """
    Connect using STORAGE_ENGINE from settings.py
    Returns sqlalchemy engine
    """
    return create_engine('sqlite:////Users/cc/projects/town-council/test_db.sqlite')


def create_tables(engine):
    Index("place_ocd_id_idx", Place.ocd_division_id)
    DeclarativeBase.metadata.create_all(engine)


class Place(DeclarativeBase):
    """Place table"""
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String)
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
    __tablename__ = 'event_stage'

    id = Column(Integer, primary_key=True)
    ocd_division_id = Column(String)
    name = Column(String)
    scraped_datetime = Column(DateTime, default=datetime.datetime.now)
    record_date = Column(Date)
    source = Column(String)
    source_url = Column(String)
    meeting_type = Column(String)


#####

class Event(DeclarativeBase):
    """Event table"""
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    ocd_division_id = Column(String)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=False)
    name = Column(String)
    scraped_datetime = Column(DateTime, default=datetime.datetime.now)
    record_date = Column(Date)
    source = Column(String)
    source_url = Column(String)
    meeting_type = Column(String)


class UrlStageHist(DeclarativeBase):
    """Url Staging History Table"""
    __tablename__ = 'url_stage_hist'

    id = Column(Integer, primary_key=True)
    ocd_division_id = Column(String)
    event = Column(String)
    event_date = Column(Date)
    url = Column(String)
    url_hash = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Catalog(DeclarativeBase):
    """Document catalog table"""
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    url_hash = Column(String, unique=True, index=True)
    location = Column(String)
    filename = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.now)


class Document(DeclarativeBase):
    """Document table"""
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False, index=True)
    catalog_id = Column(Integer, ForeignKey('catalog.id'), nullable=True, index=True)
    url = Column(String)
    url_hash = Column(String)
    media_type = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    place = relationship('Place')
    event = relationship('Event')
    catalog = relationship('Catalog')


engine = db_connect()
create_tables(engine)
