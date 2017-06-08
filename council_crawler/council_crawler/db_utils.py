import datetime
import sqlite3

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date, DateTime, MetaData, Table, String


STORAGE_ENGINE = get_project_settings().get('STORAGE_ENGINE')


def stage_url(document, event):
    """Determine storage engine in settings.py STORAGE_ENGINE
    and stage URL"""

    if STORAGE_ENGINE['drivername'] == 'sqlite':
        sqlite_stage_url(document, event)
    elif STORAGE_ENGINE['drivername'] == 'postgresql':
        pg_stage_url(document, event)


def pg_stage_url(document, event):
    """Stage URL in postgres database"""

    db, data_table = get_or_create_url_stage()
    engine = create_engine(db)

    with engine.connect() as conn:
        try:
            conn.execute(
                data_table.insert(),
                event=event['name'],
                event_date=event['record_date'],
                url=document['url'],
                url_hash=document['url_hash'],
                media_type=document['media_type'],
                category=document['category']
                )
        except Exception as e:
            print(e)


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
                media_type VARCHAR(80),
                url_hash VARCHAR(80),
                category VARCHAR(150),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
            """
            )

    cursor.execute(
        """insert into URL_STAGE (
            event, event_date, url, media_type, url_hash, category) \
        values (?, ?, ?, ?, ?, ?)
        """,
        (event['name'],
         event['record_date'],
         document['url'],
         document['media_type'],
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
    table_name = 'tc_url_stage'
    data_table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('event', String),
            Column('event_date', Date),
            Column('url', String),
            Column('url_hash', String),
            Column('category', String),
            Column('media_type', String),
            Column('created_at', DateTime, default=datetime.datetime.now)
    )
    if not engine.dialect.has_table(engine, table_name):
        data_table.create()

    return db, data_table

