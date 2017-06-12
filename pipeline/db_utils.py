import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date, DateTime, MetaData, Table, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import sql

STORAGE_ENGINE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    # 'port': '5432',
    'username': 'cc',
    # 'password': 'YOUR_PASSWORD',
    'database': 'town_council'
}


def setup_db():
    driver = STORAGE_ENGINE['drivername']
    host = STORAGE_ENGINE['host']
    username = STORAGE_ENGINE['username']
    # port = STORAGE_ENGINE['port']
    database = STORAGE_ENGINE['database']

    db = f'{driver}://{username}@{host}/{database}'
    engine = create_engine(db)
    metadata = MetaData(db)

    return engine, metadata


def get_url_stage():

    _, metadata = setup_db()

    table = Table(
            'url_stage',
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

    return table


def get_url_stage_hist():

    _, metadata = setup_db()

    table = Table(
            'url_stage_hist',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('event', String),
            Column('event_date', Date),
            Column('url', String),
            Column('url_hash', String),
            Column('category', String),
            Column('created_at', DateTime, default=datetime.datetime.now)
    )

    return table


def get_catalog():
    _, metadata = setup_db()

    table = Table(
            'catalog',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('url', String,),
            Column('url_hash', String, unique=True, index=True),
            Column('location', String),
            Column('filename', String),
            Column('uploaded_at', DateTime, default=datetime.datetime.now)
    )

    return table


def get_document():
    _, metadata = setup_db()
    catalog = get_catalog()
    place = get_place()
    event = get_event()

    table = Table(
            'document',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('place_id', Integer, ForeignKey(place.c.id),
                   nullable=False, index=True),
            Column('event_id', Integer, ForeignKey(event.c.id),
                   nullable=False, index=True),
            Column('catalog_id', Integer, ForeignKey(catalog.c.id),
                   nullable=True, index=True),
            Column('url', String),
            Column('url_hash', String),
            Column('media_type', String),
            Column('category', String),
            Column('created_at', DateTime, default=datetime.datetime.now)
    )

    return table


def get_place():
    _, metadata = setup_db()

    table = Table(
        'place',
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

    return table


def get_event():
    _, metadata = setup_db()
    place = get_place()

    table = Table(
        'event',
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

    return table


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


def get_event_id(name, record_date, place_id, engine):
    """Check if event exists and return ID or return None if not exists"""

    stmt = sql.text(
        """
        SELECT id FROM event
        WHERE place_id = :place_id
        AND name = :name
        AND record_Date = :record_date
        """
        )

    # Check does event already exists
    with engine.connect() as conn:
        result = conn.execute(
            stmt,
            place_id=place_id,
            name=name,
            record_date=record_date
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
