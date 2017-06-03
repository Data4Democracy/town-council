from council_crawler.items import Event
from council_crawler.db_utils import save_url
from council_crawler.utils import url_to_md5


class SaveMediaResourcePipeline(object):
    """Stores links to media for later download"""
    def process_item(self, item, spider):
        if isinstance(item, Event):
            if item.get('agenda_urls', None):
                for url in item['agenda_urls']:
                    media = {
                        'event': item['name'],
                        'event_date': item['record_date'],
                        'media_type': 'application/pdf',
                        'url': url,
                        'url_hash': url_to_md5(url),
                        'category': 'agenda'
                    }
                    save_url(media)
        return item
