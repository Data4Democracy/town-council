import requests
import db_utils
from sqlalchemy.orm import sessionmaker
from models import Place, UrlStage, Event, Catalog, Document, EventStage
from models import db_connect, create_tables


class Media():
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
        file_path = self._create_fp_from_ocd_id(self.doc.ocd_division_id)
        print(extension)
        if extension == 'pdf':
            with open(f'{file_path}/{url_hash}.pdf', 'wb') as f:
                f.write(content.content)
                return f.name
        if extension == 'html':
            with open (f'{file_path}/{url_hash}.html', 'w') as f:
                f.write(content.text)
                return f.name

    def _create_fp_from_ocd_id(self, ocd_id):
        elements = ocd_id.split('/')
        country = elements[1].split(':')[-1]
        state = elements[2].split(':')[-1]
        place = elements[3].split(':')[-1]

        return (f'./data/{country}/{state}/{place}')


def map_document(url_record, place_id, event_id, catalog_id):
    document = Document(
        place_id=place_id,
        event_id=event_id,
        catalog_id=catalog_id,
        url=url_record.url,
        url_hash=url_record.url_hash,
        media_type='',
        category=url_record.category
        )
    return document


def save_record(record):
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.add(record)
        session.commit()
        return record.id
    except:
        session.rollback()
        raise
    finally:
        session.close()
        print('Session closed')


def copy_event_from_stage(staged_event):
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    place = session.query(Place) \
        .filter(Place.ocd_division_id == staged_event.ocd_division_id).first()

    event = Event(
        ocd_division_id=staged_event.ocd_division_id,
        place_id=place.id,
        name=staged_event.name,
        scraped_datetime=staged_event.scraped_datetime,
        record_date=staged_event.record_date,
        source=staged_event.source,
        source_url=staged_event.source_url,
        meeting_type=staged_event.meeting_type
    )
    event = save_record(event)
    return event


def process_staged_urls():
    """Query download all staged URLs, Update Catalog and Document"""

    engine = db_connect()
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # for event in session.query(EventStage).all():
    #     copy_event_from_stage(event)

    for url_record in session.query(UrlStage).all():
        # print(url_record.url)

        place_record = session.query(Place). \
            filter(Place.ocd_division_id == url_record.ocd_division_id).first()
        event_record = session.query(Event). \
            filter(Event.ocd_division_id == url_record.ocd_division_id,
                   Event.record_date == url_record.event_date,
                   Event.name == url_record.event).first()
        print(f'place id: {place_record.id}\n event_id:{event_record.id}')

        catalog_entry = session.query(Catalog). \
            filter(Catalog.url_hash == url_record.url_hash).first()

        # Document already exists in catalog
        if catalog_entry:
            catalog_id = catalog_entry.id
            print(f'catalog_id---------{catalog_id}')
            document = map_document(
                url_record, place_record.id, event_record.id, catalog_id)
            save_record(document)
            print("existing in catalog adding reference to document")

        else:
            print("Does not exist")

            # Download and save document
            catalog = Catalog(
                url=url_record.url,
                url_hash=url_record.url_hash,
                location='placeholder',
                filename=f'{url_record.url_hash}.pdf'
                )

            doc = Media(url_record)

            # download
            result = doc.gather()

            # Add to doc catalog
            if result:
                catalog.location = result
                catalog_id = save_record(catalog)
                # Add document reference
                document = map_document(
                    url_record, place_record.id, event_record.id, catalog_id)
                doc_id = save_record(document)

                print(f'Added {url_record.url_hash} doc_id: {doc_id}')

    # # cleanup
    # archive_url_stage()


def archive_url_stage():
    """Copy staging records to history table and clear staging table"""
    engine, _ = db_utils.setup_db()
    conn = engine.connect()

    conn.execute("insert into url_stage_hist (select * from url_stage)")
    conn.execute("delete from url_stage")


def create_document_metadata(url_record, catalog_id, place_id, event_id):
    metadata = dict(
        place_id=place_id,
        event_id=event_id,
        catalog_id=catalog_id,
        url=url_record.url,
        url_hash=url_record.url_hash,
        media_type='',
        category=url_record.category,

        )
    return metadata


def add_document_metadata(conn, document_db, metadata):
    # TODO Add media type
    # TODO prevent dupes
    metadata_id = conn.execute(
        document_db.insert().returning(document_db.c.id),
        place_id=metadata['place_id'],
        event_id=metadata['event_id'],
        catalog_id=metadata['catalog_id'],
        url=metadata['url'],
        url_hash=metadata['url_hash'],
        media_type='placeholder',
        category=metadata['category'],
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

process_staged_urls()


# db_utils.create_tables()
