import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url

import scrapy

from council_crawler.items import Event
from council_crawler.utils import url_to_md5, parse_date_string

class LegistarCms(scrapy.spiders.CrawlSpider):
    name = 'legistar_cms'
    ocd_division_id = ''
    formatted_city_name = ''
    city_name = ''
    urls = []

    def __init__(self, legistar_url='', city='', state='', *args, **kwargs):
        super(LegistarCms, self).__init__(*args, **kwargs)
        self.urls = [legistar_url]
        if not self.urls:
            raise ValueError('legistar_url is required.')
        if not city:
            raise ValueError('city is required')

        self.city_name = city.lower()

        if not state:
            raise ValueError('state is required.')
        if len(state) is not 2:
            raise ValueError('state must be a two letter abbreviation.')
      
        self.formatted_city_name = '{}, {}'.format(
            self.city_name.title(), state.upper())
        self.ocd_division_id = 'ocd-division/country:us/state:{}/place:{}'.format(
            state.lower(), self.city_name.replace(' ', '_'))

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_archive)

    def parse_archive(self, response):
        archive_base_url = get_base_url(response)

        def get_agenda_url(relative_urls):
            full_url = []
            if relative_urls:
                for url in relative_urls:
                    url = urljoin(archive_base_url, url)
                    full_url.append(url)
                return full_url

        table_body = response.xpath('//table[@class="rgMasterTable"]/tbody/tr')
        for row in table_body:
            # most elements are wrapped in <font> tags that aren't
            # visible when viewing in e.g. Chrome debugger
            meeting_type = row.xpath('.//td[1]/font/a/font/text()').extract_first()
            date = row.xpath('.//td[2]/font/text()').extract_first()
            time = row.xpath('.//td[4]/font/span/font/text()').extract_first()
            date_time = '{} {}'.format(date, time)
            agenda_url = row.xpath('.//td[7]/font/span/a/@href').extract_first()
            event_minutes_url = row.xpath('.//td[8]/font/span/a/font/text()').extract_first()
            # if there are no minutes the data will be 'Not\xa0available' (with unicode space)
            if event_minutes_url == 'Not\xa0available':
                event_minutes_url = None

            event = Event(
                _type='event',
                ocd_division_id=self.ocd_division_id,
                name='{} City Council {}'.format(self.formatted_city_name, meeting_type),
                scraped_datetime=datetime.datetime.utcnow(),
                record_date=parse_date_string(date_time),
                source=self.city_name,
                source_url=response.url,
                meeting_type=meeting_type
                )

            documents = []
            if agenda_url is not None:
                # If path to agenda is relative, complete it with the base url
                if archive_base_url not in agenda_url:
                    agenda_url = urljoin(archive_base_url, agenda_url)
                agenda_doc = {
                    'url': agenda_url,
                    'url_hash': url_to_md5(agenda_url),
                    'category': 'agenda'
                }
                documents.append(agenda_doc)

            if event_minutes_url is not None:
                # If path to minutes is relative, complete it with the base url
                if archive_base_url not in event_minutes_url:
                    event_minutes_url = urljoin(archive_base_url, event_minutes_url)
                minutes_doc = {
                    'url': event_minutes_url,
                    'url_hash': url_to_md5(event_minutes_url),
                    'category': 'minutes'
                }
                documents.append(minutes_doc)

            event['documents'] = documents
            yield event
