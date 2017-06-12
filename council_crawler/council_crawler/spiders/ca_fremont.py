import datetime
from urllib.parse import urljoin

import scrapy

from council_crawler.items import Event
from council_crawler.utils import url_to_md5


class Dublin(scrapy.spiders.CrawlSpider):
    name = 'fremont'
    base_url = 'https://fremont.gov/AgendaCenter/'

    def start_requests(self):

        urls = [self.base_url]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_archive)

    def parse_archive(self, response):

        def get_agenda_url(relative_urls):
            full_url = []
            if relative_urls:
                for url in relative_urls:
                    if self.base_url not in url:
                        url = urljoin(self.base_url, url)
                    full_url.append(url)
                return full_url
            else:
                return None

        containers = response.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " listing ")]')
        for table in containers:
            table_body = table.xpath('.//table/tbody/tr')
            meeting_type = table.xpath('.//h2/text()').extract_first()
            for row in table_body:
                record_date = row.xpath('.//td[1]/h4/a[2]/strong/abbr/text()').extract_first() + \
                    " " + row.xpath('.//td[1]/h4/a[2]/strong/text()').extract_first()
                record_date = datetime.datetime.strptime(record_date, '%b %d, %Y').date()
                agenda_urls = row.xpath(
                    './/td[@class="downloads"]/div/div/div/div/ol/li/a/@href').extract()
                agenda_urls = get_agenda_url(agenda_urls)
                minutes_url = row.xpath('.//td[@class="minutes"]/a/@href').extract_first()

                event = Event(
                    _type='event',
                    name='Fremont, CA City Council {}'.format(meeting_type),
                    scraped_datetime=datetime.datetime.utcnow(),
                    record_date=record_date,
                    source=self.name,
                    source_url=response.url,
                    meeting_type=meeting_type,
                    )

                # This block should be cleaned up later
                # create nested JSON obj for each doc related to meeting
                documents = []
                if agenda_urls is not None:
                    for url in agenda_urls:
                        agenda_doc = {
                            'media_type': 'application/pdf',
                            'url': url,
                            'url_hash': url_to_md5(url),
                            'category': 'agenda'
                        }
                        documents.append(agenda_doc)

                if minutes_url is not None:
                    if self.base_url not in minutes_url:
                        minutes_url = urljoin(self.base_url, minutes_url)
                    minutes_doc = {
                        'media_type': 'application/pdf',
                        'url': url,
                        'url_hash': url_to_md5(minutes_url),
                        'category': 'minutes'
                    }
                    documents.append(minutes_doc)

                event['documents'] = documents

                yield event
