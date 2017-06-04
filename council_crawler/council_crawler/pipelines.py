from council_crawler.items import Event
from council_crawler.db_utils import save_url
from council_crawler.utils import url_to_md5


class SaveDocumentLinkPipeline(object):
    """Stores links to media"""
    def process_item(self, item, spider):
        if isinstance(item, Event):
            for doc in item['documents']:
                save_url(doc, item)
        return item

