import sqlite3

import requests


def process_docs(docs):
    session = requests.Session()
    for doc in docs:
        content = get_document(session, doc[3])
        result = store_document(content, doc[4], doc[5])
        print(result)


def get_document(session, document_url):
    r = session.get(document_url)
    if r.ok:
        return r


def store_document(content, type, url_hash):
    type = type.split("/")[-1]
    if type == 'pdf':
        with open(f'{url_hash}.pdf', 'wb') as f:
            f.write(content.content)
            return f
    if type == 'html':
        with open (f'{url_hash}.html', 'w') as f:
            f.write(content.text)
            return f


database = 'town_council.sqlite'

connection = sqlite3.connect(database)
cursor = connection.cursor()
cursor.execute("select * from URL_STAGE")

process_docs(cursor)



# Get / Receive links
# Parse for URL
# Download
# Store
# Update DB with result

