import requests


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


# Get / Receive links
# Parse for URL
# Download
# Store
# Update DB with result

