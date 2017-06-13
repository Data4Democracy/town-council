import requests
import db_utils
from sqlalchemy.sql import select


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

    engine, _ = db_utils.setup_db()
    conn = engine.connect()
    url_stage = db_utils.get_url_stage()
    catalog = db_utils.get_catalog()
    document_db = db_utils.get_document()

    select_all_url_stage = select([url_stage])
    for url_record in conn.execute(select_all_url_stage).fetchall():
        print(url_record)
        place_id = db_utils.get_place_id(url_record['ocd_division_id'])
        event_id = db_utils.get_event_id(
            url_record['event'], url_record['event_date'], place_id, engine)

        select_by_hash = select([catalog]). \
            where(catalog.c.url_hash == url_record.url_hash)

        result = conn.execute(select_by_hash).first()
        if result:
            # Document already exists in catalog
            catalog_id = result.id
            metadata = create_document_metadata(url_record, catalog_id, place_id, event_id)
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
                metadata = create_document_metadata(url_record, catalog_id, place_id, event_id)
                metadata_id = add_document_metadata(conn, document_db, metadata)
                print(f'Added {metadata_id}: {url_record.url_hash}')

    # cleanup
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
