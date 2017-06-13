import datetime

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date, DateTime, MetaData, Table, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import sql


def stage_url(document, event):
    """Stage URL in postgres database"""

    engine, _ = setup_db()
    staging_table = get_url_stage()

    with engine.connect() as conn:
        conn.execute(
            staging_table.insert(),
            ocd_division_id=event['ocd_division_id'],
            event=event['name'],
            event_date=event['record_date'],
            url=document['url'],
            url_hash=document['url_hash'],
            category=document['category']
        )


def get_or_create_event(event):
    """Create event and return new ID or return ID if exists"""
    engine, _ = setup_db()
    event_table = get_event()
    place_id = get_place_id(event['ocd_division_id'])
    event_id = get_event_id(event, place_id, engine)

    # create event if does not exist
    if event_id is None:
        create_event(event, place_id, event_table, engine)

        # re-query to stay compatabile with sqlite syntax
        event_id = get_event_id(event, place_id, engine)
    return event_id


def create_event(event, place_id, event_table, engine):
    """Create event"""
    with engine.connect() as conn:
        result = conn.execute(
            event_table.insert(),
            place_id=place_id,
            name=event['name'],
            scraped_datetime=event['scraped_datetime'],
            record_date=event['record_date'],
            source=event['source'],
            source_url=event['source_url'],
            meeting_type=event['meeting_type']
        )
    return result


def get_event_id(event, place_id, engine):
    """Check if event exists and return ID or return None if not exists"""

    stmt = sql.text(
        """
        SELECT id FROM event
        WHERE place_id = :place_id
        AND name = :name
        AND record_Date = :record_date
        """
        )

    # Check if event already exists
    with engine.connect() as conn:
        result = conn.execute(
            stmt,
            place_id=place_id,
            name=event['name'],
            record_date=event['record_date']
        ).first()
    if result:
        return result.id
    else:
        return None


def get_place_id(ocd_division_id):
    engine, _ = setup_db()
    place_table = get_place()

    with engine.connect() as conn:
        by_ocd_id = sql.select([place_table.c.id]) \
            .where(place_table.c.ocd_division_id == ocd_division_id)
        place_id = conn.execute(by_ocd_id).first()

    return place_id.id


def get_url_stage():
    """Return URL staging table"""
    _, metadata = setup_db()
    table_name = 'url_stage'

    url_stage_table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('ocd_division_id', String),
            Column('event', String),
            Column('event_date', Date),
            Column('url', String),
            Column('url_hash', String),
            Column('category', String),
            Column('created_at', DateTime, default=datetime.datetime.now)
    )

    return url_stage_table


def get_event():
    """Return event table"""
    _, metadata = setup_db()
    place = get_place()
    table_name = 'event'

    event_table = Table(
        table_name,
        metadata,
        Column('id', Integer, primary_key=True),
        Column('place_id', Integer, ForeignKey(place.c.id),
               nullable=False, index=True),
        Column('name', String),
        Column('scraped_datetime', DateTime, default=datetime.datetime.now),
        Column('record_date', Date),
        Column('source', String),
        Column('source_url', String),
        Column('meeting_type', String)
        )

    return event_table


def get_place():
    """Return place table"""
    _, metadata = setup_db()
    table_name = 'place'

    place_table = Table(
        table_name,
        metadata,
        Column('id', Integer, primary_key=True),
        Column('place', String),
        Column('type', String),
        Column('state', String),
        Column('country', String),
        Column('display_name', String),
        Column('ocd_division_id', String, index=True),
        Column('seed_url', String),
        Column('hosting_service', String),
        Column('crawler', Boolean, default=False),
        Column('crawler_name', String),
        Column('crawler_type', String),
        Column('crawler_owner', String)
    )

    return place_table


def setup_db():
    """Setup database specified in STORAGE_ENGINE in settings.py"""
    db = get_project_settings().get('STORAGE_ENGINE')
    engine = create_engine(db)
    metadata = MetaData(db)

    return engine, metadata

def create_tables():
    engine, metadata = setup_db()

    url_stage = get_url_stage()
    url_stage_hist = get_url_stage_hist()
    catalog = get_catalog()
    place = get_place()
    document = get_document()
    event = get_event()

    if not engine.dialect.has_table(engine, url_stage):
        url_stage.create()
    if not engine.dialect.has_table(engine, catalog):
        catalog.create()
    if not engine.dialect.has_table(engine, url_stage_hist):
        url_stage_hist.create()
    if not engine.dialect.has_table(engine, place):
        place.create()
    if not engine.dialect.has_table(engine, event):
        event.create()
    if not engine.dialect.has_table(engine, document):
        document.create()
