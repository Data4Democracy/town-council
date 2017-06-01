import datetime
from urllib.parse import urljoin

import scrapy
from council_crawler.items import Record

class Belmont(scrapy.spiders.CrawlSpider):
	name = 'belmont'

	def start_requests(self):

		urls = ['http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all']

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse_archive)

	def parse_archive(self, response):

		def get_agenda_url(relative_urls):
			full_url = []
			if relative_urls:
				for url in relative_urls:
					base_url = 'http://belmont.gov'
					url = urljoin(base_url, url)
					full_url.append(url)
				return full_url
			else:
				None

		table_body = response.xpath('//table/tbody/tr')
		#print(table_body)
		for row in table_body:
			print(row.xpath('.//td'))
			event_url = row.xpath('.//td[@class="event_title"]//a/@href').extract_first()
			date_time = row.xpath('.//td[@class="event_datetime"]/text()').extract_first()
			agenda_url = row.xpath('.//td[@class="event_agenda"]//a/@href').extract_first()
			event_minutes_url = row.xpath('.//td[@class="event_minutes"]/a/@href').extract_first()
			event_video_url = row.xpath('.//td[@class="event_video"]//a/@href').extract_first()

			record = Record(
				scraped_datetime = datetime.datetime.utcnow(),
				record_date = date_time,
				#event_url = event_url,
				source = self.name,
				source_url = response.url,
				#event_datetime = datetime,
				agenda_url = agenda_url if agenda_url else None,
				minutes_url = event_minutes_url if event_minutes_url else None,
				video_url = event_video_url if event_video_url else None,	
				)
			yield record