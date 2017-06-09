## Basic Structure:
* See scrapy architecture [overview](https://doc.scrapy.org/en/1.2/topics/architecture.html)
* Each municipality will have a custom spider `council_crawler/spiders/<state>_<muni.municipality>.py` which contains rules specific to collecting links, documents and parsing information contained in that site.
* Our first goal is to write a spider to return an `Event` [item](https://doc.scrapy.org/en/latest/topics/items.html) (see `items.py`) which will be be validated and saved by shared logic in `pipeline.py`.

For now spider just returns a json object which can be output to a file by running the below command in `town-council/council_crawler` directory (requires environment with scrapy v1.4 installed -- `pip install scrapy`):

`scrapy crawl dublin -o test.json`

Example of record item from [Belmont, CA](http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all/-npage-2)

```
{

    "_type": "event",
    "name": "Belmont, CA City Council Parks and Recreation Commission Meeting",
    "scraped_datetime": "2017-06-03 11:03:44",
    "record_date": "04/05/2017 7:00 PM ",
    "source": "belmont",
    "source_url": "http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all/-npage-2",
    "meeting_type": "Parks and Recreation Commission Meeting",
    "documents": [
        {
            "url": "http://belmont-ca.granicus.com/GeneratedAgendaViewer.php?event_id=2d488f17-13ff-11e7-ad57-f04da2064c47",
            "url_hash": "8dc13790ccd0c186275c4d67ae4bf69a",
            "category": "agenda"
        },
        {
            "url": "/Home/ShowDocument?id=15369",
            "url_hash": "d88e4b232a72b0522a4cce17521654f5",
            "category": "minutes"
        }
    ]

}
```

TBD: Once this metadata is stored, intention is to use this information to schedule download of documents contained in found at `documents` field.

We are slowly working towards implementing [Open Civic Data's standard data formats](http://opencivicdata.readthedocs.io/en/latest/data/index.html) but because our goal primarily to gather a list of documents (specifically town council minutes and agenda's) we do not use all fields. However, when possible it is beneficial to use standards set by people with lots of experience in this domain.

### Event Objects

Event is a scrapy item object loosely based on Open Civic Data's [Event]object (http://opencivicdata.readthedocs.io/en/latest/data/event.html)

Changes to the Event schema will impact ALL spiders. We are open to suggestions or improvements but any changes should be cleared with maintainers prior to starting work.

**Required Fields**  
**_type:** string always set to `event`  
**name:** string describing name of event. Generally the name as it appears on the website  
**scraped_datetime:** datetime spider ran in YYYY-MM-DD HH:MM:SS should be standardized to UTC  
**source_url:** URL or landing page the event item was gathered from  
**source:** spider name  

**Optional Fields:**  
**record_date:** Start date/time of meeting if it can be determined YYYY-MM-DD HH:MM:SS should be standardized to UTC  
**documents:** list of `media_items` (see below)  
**meeting_type:** General text name of meeting. Ex: Town Council General Meeting or Parks and Recreation Commission Meeting  

### Media Objects  
Nested json object which contains documents identified as being linked to a particular events. Agendas, meeting minutes, supporting documentation such as building permits/plans etc.

**Fields:**  
**url:** URL of document. If possible follow redirects to get final resource location  
**url_hash:** MD5 of hash, used further downstream to dedupe & organize download of docs  
**category:** Document category. Ex agenda, minutes. Types to be added as encountered  

Example media objects
```
{
    "url": "http://belmont-ca.granicus.com/GeneratedAgendaViewer.php?event_id=2d488f17-13ff-11e7-ad57-f04da2064c47",
    "url_hash": "8dc13790ccd0c186275c4d67ae4bf69a",
    "category": "agenda"
}

{
    "url": "/Home/ShowDocument?id=15369",
    "url_hash": "d88e4b232a72b0522a4cce17521654f5",
    "category": "minutes"
}
```

### Additional settings  

Work in progress. Currently supports sqlite & postgresql.

`STORAGE_ENGINE` is a dictionary containing the connection details needed to connect/create database used by `SaveDocumentLinkPipeline` to store document links the spiders have collected.

```
# sqlite template
STORAGE_ENGINE = {
    'drivername': 'sqlite',
    'database': 'town_council.sqlite'
}
```

```
# postgresql template
STORAGE_ENGINE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'USERNAME',
    'password': 'YOUR_PASSWORD',
    'database': 'town_council'
}
```
