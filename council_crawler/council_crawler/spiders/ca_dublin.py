import datetime
from urllib.parse import urljoin

import scrapy

from council_crawler.items import Event
from council_crawler.utils import url_to_md5


class Dublin(scrapy.spiders.CrawlSpider):
    name = 'dublin'

    def start_requests(self):

        urls = ['http://dublinca.gov/1604/Meetings-Agendas-Minutes-Video-on-Demand']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_archive)

    def parse_archive(self, response):

        def get_agenda_url(relative_urls):
            full_url = []
            if relative_urls:
                for url in relative_urls:
                    base_url = 'http://dublinca.gov'
                    url = urljoin(base_url, url)
                    full_url.append(url)
                return full_url
            else:
                return None

        table_body = response.xpath('//table/tbody/tr')
        for row in table_body:
            record_date = row.xpath('.//td[@data-th="Date"]/text()').extract_first()
            record_date = datetime.datetime.strptime(record_date, '%B %d, %Y')

            meeting_type = row.xpath('.//td[@data-th="Meeting Type"]/text()').extract_first()
            agenda_urls = row.xpath('.//td[starts-with(@data-th,"Agenda")]/a/@href').extract()
            agenda_urls = get_agenda_url(agenda_urls)
            minutes_url = row.xpath('.//td[@data-th="Minutes"]/a/@href').extract_first()

            event = Event(
                _type='event',
                name='Dublin, CA City Council {}'.format(meeting_type),
                scraped_datetime=datetime.datetime.utcnow(),
                record_date=record_date,
                source=self.name,
                source_url=response.url,
                meeting_type=meeting_type,
                )

            # This block should be cleaned up later
            # create nested JSON obj for each doc related to meeting
            documents = []
            for url in agenda_urls:
                agenda_doc = {
                    'media_type': 'application/pdf',
                    'url': url,
                    'url_hash': url_to_md5(url),
                    'category': 'agenda'
                }
                documents.append(agenda_doc)

            minutes_doc = {
                'media_type': 'application/pdf',
                'url': minutes_url,
                'url_hash': url_to_md5(url),
                'category': 'minutes'
            }
            documents.append(minutes_doc)

            event['documents'] = documents

            yield event
