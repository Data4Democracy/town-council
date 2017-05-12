## Basic Structure:  
* See scrapy architecture [overview](https://doc.scrapy.org/en/1.2/topics/architecture.html)
* Each municipality will have a custom spider `council_crawler/spiders/<state>_<muni.municipality>.py` which contains rules specific to collecting links, documents and parsing information contained in that site.
* All spiders will return a Record [item](https://doc.scrapy.org/en/latest/topics/items.html) (see `items.py`) which will be be validated and saved by shared logic in `pipeline.py`. 

For now spider just returns a json object which can be output to a file by running the below command in `town-council/council_crawler` directory (requires environment with scrapy v1.3 installed -- `pip install scrapy`):

`scrapy crawl dublin -o test.json`

Example of record item from http://dublinca.gov/1604/Meetings-Agendas-Minutes-Video-on-Demand

```
{'agenda_url': ['http://dublinca.gov/Archive.aspx?ADID=736'],
 'meeting_type': 'Regular Meeting',
 'minutes_url': 'http://www.pbtech.org/clients/dublin_cc/dublinccm02212017.html',
 'record_date': 'February 21, 2017',
 'scraped_datetime': '2017-05-12 12:43:27',
 'source': 'dublin',
 'source_url': 'http://dublinca.gov/1604/Meetings-Agendas-Minutes-Video-on-Demand',
 'video_url': 'http://www.pbtech.org/clients/dublin_cc/dublincc02212017.html'}
 ```

TBD: Once this metadata is stored, intention is to use this information to schedule download of pdfs found at `minutes_url, agenda_url(s)` etc.