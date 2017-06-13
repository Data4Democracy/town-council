import datetime
import sqlite3

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date, DateTime, MetaData, Table, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import sql

STORAGE_ENGINE = get_project_settings().get('STORAGE_ENGINE')


def stage_url(document, event):
    """Determine storage engine in settings.py STORAGE_ENGINE
    and stage URL"""

    if STORAGE_ENGINE['drivername'] == 'sqlite':
        sqlite_stage_url(document, event)
    elif STORAGE_ENGINE['drivername'] == 'postgresql':
        pg_stage_url(document, event)


def get_or_create_event(event):
    """Create event and return ID, return ID if event exists"""
    engine, _ = setup_db()
    event_table = get_event()
    place_id = get_place_id(event['ocd_division_id'])

    event_id = get_event_id(event, place_id, engine)

    if event_id is None:
        # create event if does not exist
        event_id = create_event(event, place_id, event_table, engine)
        event_id = event_id.first().id

    return event_id


def create_event(event, place_id, event_table, engine):

    with engine.connect() as conn:
        result = conn.execute(
            event_table.insert().returning(event_table.c.id),
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


def pg_stage_url(document, event):
    """Stage URL in postgres database"""

    db, data_table = get_or_create_url_stage()
    engine = create_engine(db)

    with engine.connect() as conn:
        conn.execute(
            data_table.insert(),
            ocd_division_id=event['ocd_division_id'],
            event=event['name'],
            event_date=event['record_date'],
            url=document['url'],
            url_hash=document['url_hash'],
            category=document['category']
        )


def get_place_id(ocd_division_id):
    engine, _ = setup_db()
    place_table = get_place()

    with engine.connect() as conn:
        by_ocd_id = sql.select([place_table.c.id]) \
            .where(place_table.c.ocd_division_id == ocd_division_id)
        place_id = conn.execute(by_ocd_id).first()

    return place_id.id


def sqlite_stage_url(document, event):
    """Stage URL to temp sqlite database

    Used for testing and prototyping.

    #TODO convert to SQLALCHEMY
    """

    conn_str = f"{STORAGE_ENGINE['database']}.sqlite"
    connection = sqlite3.connect(conn_str)
    cursor = connection.cursor()
    cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS URL_STAGE(
                id INTEGER PRIMARY KEY,
                event VARCHAR(80),
                event_date DATE,
                url VARCHAR(80),
                url_hash VARCHAR(80),
                category VARCHAR(150),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
            """
            )

    cursor.execute(
        """insert into URL_STAGE (
            event, event_date, url, url_hash, category) \
        values (?, ?, ?, ?, ?)
        """,
        (event['name'],
         event['record_date'],
         document['url'],
         document['url_hash'],
         document['category']))
    connection.commit()
    return event


def get_or_create_url_stage():
    """Return database & URL staging table
    Create table if does not exist"""

    driver = STORAGE_ENGINE['drivername']
    host = STORAGE_ENGINE['host']
    username = STORAGE_ENGINE['username']
    # port = STORAGE_ENGINE['port']
    database = STORAGE_ENGINE['database']

    db = f'{driver}://{username}@{host}/{database}'
    # db = 'postgresql://cc@localhost/cc'
    engine = create_engine(db)
    metadata = MetaData(db)
    table_name = 'url_stage'
    data_table = Table(
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
    if not engine.dialect.has_table(engine, table_name):
        data_table.create()

    return db, data_table


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
