from council_crawler.items import Event
from council_crawler.db_utils import stage_url, get_or_create_event


class SaveDocumentLinkPipeline(object):
    """Stores links to media"""
    def process_item(self, item, spider):
        if isinstance(item, Event):

            # TODO get or create
            get_or_create_event(item)
            for doc in item['documents']:
                stage_url(doc, item)
        return item
