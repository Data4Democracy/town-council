import datetime

import requests
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date, DateTime, MetaData, Table, String
from sqlalchemy import ForeignKey
from sqlalchemy.sql import select


# TODO create event table

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
        self.response = self._get_document(self.doc.url)
        if self.response:
            content_type = self._parse_content_type(self.response.headers)
            file_location = self._store_document(
                    self.response, content_type, self.doc.url_hash)
            return file_location
        else:
            return None

    def validate(self):
        pass

    def store(self):
        pass

    def cleanup(self):
        pass

    def _parse_content_type(self, headers):
        """Parse response headers to get Content-Type"""
        content_type = None
        content_type = headers.get('Content-Type', None)
        if content_type:
            content_type = content_type.split(';')[0]  # 'text/html; charset=utf-8'
            content_type = content_type.split('/')[-1]  # text/html
        return content_type

    def _get_document(self, document_url):
        try:
            r = self.session.get(document_url)
            if r.ok:
                return r
            else:
                return r.status_code
        except requests.exceptions.MissingSchema as e:
            print(e)
            return None

    def _store_document(self, content, content_type, url_hash):
        extension = content_type.split(';')[0].split('/')[-1]
        print(extension)
        if extension == 'pdf':
            with open(f'./data/{url_hash}.pdf', 'wb') as f:
                f.write(content.content)
                return f.name
        if extension == 'html':
            with open (f'./data/{url_hash}.html', 'w') as f:
                f.write(content.text)
                return f.name


def process_staged_urls():
    """Query download all staged URLs, Update Catalog and Document"""

    # TODO Break up function

    engine, _ = setup_db()
    conn = engine.connect()
    url_stage = get_url_stage()
    catalog = get_catalog()
    document_db = get_document(catalog)

    select_all_url_stage = select([url_stage])
    for url_record in conn.execute(select_all_url_stage).fetchall():
        select_by_hash = select([catalog]). \
            where(catalog.c.url_hash == url_record.url_hash)
        result = conn.execute(select_by_hash).first()
        if result:
            # Document already exists in catalog
            catalog_id = result.id
            metadata = create_document_metadata(url_record, catalog_id)
            metadata_id = add_document_metadata(conn, document_db, metadata)
            print("existing in catalog adding reference to document")

        else:
            # Download and save document
            entry = dict(
                url=url_record.url,
                url_hash=url_record.url_hash,
                filename=f'{url_record.url_hash}.pdf')

            doc = Document(url_record)

            # download
            result = doc.gather()

            # Add to doc catalog
            if result:
                entry['location'] = result
                catalog_id = add_catalog_entry(conn, catalog, entry)

                # Add document reference
                metadata = create_document_metadata(url_record, catalog_id)
                metadata_id = add_document_metadata(conn, document_db, metadata)
                print(f'Added {metadata_id}: {url_record.url_hash}')

    # cleanup
    archive_url_stage()


def archive_url_stage():
    """Copy staging records to history table and clear staging table"""
    engine, _ = setup_db()
    conn = engine.connect()

    conn.execute("insert into url_stage_hist (select * from url_stage)")
    conn.execute("delete from url_stage")


def create_document_metadata(url_record, catalog_id):
    metadata = dict(
        event=url_record.event,
        event_date=url_record.event_date,
        url=url_record.url,
        url_hash=url_record.url_hash,
        category=url_record.category,
        status='Remove',
        doc_id=catalog_id
        )
    return metadata


def add_document_metadata(conn, document_db, metadata):
    # TODO Add media type
    # TODO prevent dupes
    metadata_id = conn.execute(
        document_db.insert().returning(document_db.c.id),
        event=metadata['event'],
        event_date=metadata['event_date'],
        url=metadata['url'],
        url_hash=metadata['url_hash'],
        media_type='placeholder',
        category=metadata['category'],
        status=metadata['status'],
        doc_id=metadata['doc_id']
        ).first().id
    return metadata_id


def add_catalog_entry(conn, catalog, entry):
    catalog_id = conn.execute(
        catalog.insert().returning(catalog.c.id),
        url=entry['url'],
        url_hash=entry['url_hash'],
        location=entry['location'],
        filename=entry['filename'],
        ).first().id
    return catalog_id


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
    url_stage_hist = get_url_stage_hist()
    catalog = get_catalog()
    document = get_document(catalog)

    if not engine.dialect.has_table(engine, url_stage):
        url_stage.create()
    if not engine.dialect.has_table(engine, catalog):
        catalog.create()
    if not engine.dialect.has_table(engine, document):
        document.create()
    if not engine.dialect.has_table(engine, url_stage_hist):
        url_stage_hist.create()


# create_tables()
process_staged_urls()
