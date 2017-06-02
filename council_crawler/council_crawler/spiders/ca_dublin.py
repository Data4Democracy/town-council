import datetime
import hashlib
from urllib.parse import urljoin

import scrapy
from council_crawler.items import Record, Link


def url_to_md5(url):
    m = hashlib.md5()
    m.update(url.encode())
    return m.hexdigest()



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
            video_url = row.xpath('.//td[@data-th="Video"]/a/@href').extract_first()
            minutes_url = row.xpath('.//td[@data-th="Minutes"]/a/@href').extract_first()

            record = Record(
                scraped_datetime = datetime.datetime.utcnow(),
                record_date = record_date,
                source = self.name,
                source_url = response.url,
                meeting_type = meeting_type,
                agenda_url = get_agenda_url(agenda_urls),
                video_url = video_url if video_url else None,  # not available immediately
                minutes_url = minutes_url if minutes_url else None,  # not available immediately
                )

            str_date = '{}_{}_{}'.format(record_date.year, record_date.month, record_date.day)

            if minutes_url:
                link = Link(
                        event='dublin_ca_{}_{}'.format(meeting_type.lower(), str_date),
                        media_type='application/pdf',
                        url=minutes_url,
                        url_hash = url_to_md5(minutes_url),
                        text = meeting_type
                    )
                yield link

            yield record

