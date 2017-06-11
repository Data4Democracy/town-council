import datetime

import requests
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date, DateTime, MetaData, Table, String
from sqlalchemy import ForeignKey
from sqlalchemy.sql import select


STORAGE_ENGINE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    # 'port': '5432',
    'username': 'cc',
    # 'password': 'YOUR_PASSWORD',
    'database': 'town_council'
}


class Document():
    def __init__(self, doc):
        self.working_dir = './data'
        self.doc = doc
        self.session = requests.Session()

    def gather(self):
        # Check if exists
        self.response = self._get_document(self.doc[3])
        self.result = self._store_document(
                self.response, self.doc[4], self.doc[5])

    def validate(self):
        pass

    def store(self):
        pass

    def cleanup(self):
        pass

    def _get_document(self, document_url):
        r = self.session.get(document_url)
        if r.ok:
            return r

    def _store_document(self, content, type, url_hash):
        type = type.split("/")[-1]
        if type == 'pdf':
            with open(f'./data/{url_hash}.pdf', 'wb') as f:
                f.write(content.content)
                return f
        if type == 'html':
            with open (f'./data/{url_hash}.html', 'w') as f:
                f.write(content.text)
                return f


def links_to_process():
    engine, _ = setup_db()
    conn = engine.connect()
    url_stage = get_url_stage()
    catalog = get_catalog()

    select_all_url_stage = select([url_stage])
    for url_record in conn.execute(select_all_url_stage).fetchall():
        select_by_hash = select([catalog]). \
            where(catalog.c.url_hash == url_record.url_hash)
        result = conn.execute(select_by_hash).first()
        if result:
            print(result)
            # Add to event document list with catalog ID
        else:
            entry = dict(
                url=url_record.url,
                url_hash=url_record.url_hash,
                location='placeholder',
                filename=f'{url_record.url_hash}.pdf')

            # Download
            # Push to S3?
            # Add to catalog
            create_catalog_entry(catalog, conn, entry)
            print(f'Added: {url_record.url_hash}')


def create_catalog_entry(catalog, conn, entry):
    conn.execute(
        catalog.insert(),
        url=entry['url'],
        url_hash=entry['url_hash'],
        location=entry['location'],
        filename=entry['filename'],
        )



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


def get_document(catalog):
    _, metadata = setup_db()
    catalog = get_catalog()

    table = Table(
            'document',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('event', String),
            Column('event_date', Date),
            Column('url', String),
            Column('url_hash', String),
            Column('media_type', String),
            Column('category', String),
            Column('status', String),
            Column('doc_id', Integer, ForeignKey(catalog.c.id),
                    nullable=True, index=True),
            Column('created_at', DateTime, default=datetime.datetime.now)
    )

    return table


def create_tables():
    engine, metadata = setup_db()

    url_stage = get_url_stage()
    catalog = get_catalog()
    document = get_document(catalog)

    if not engine.dialect.has_table(engine, url_stage):
        url_stage.create()
    if not engine.dialect.has_table(engine, catalog):
        catalog.create()
    if not engine.dialect.has_table(engine, document):
        document.create()

links_to_process()
