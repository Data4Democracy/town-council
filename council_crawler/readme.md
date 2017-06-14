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
    "ocd_division_id": "ocd-division/country:us/state:ca/place:dublin",
    "name": "Dublin, CA City Council Regular Meeting",
    "scraped_datetime": "2017-06-12 22:48:44",
    "record_date": "2017-02-07",
    "source": "dublin",
    "source_url": "http://dublinca.gov/1604/Meetings-Agendas-Minutes-Video-on-Demand",
    "meeting_type": "Regular Meeting",
    "documents": [
        {
            "url": "http://dublinca.gov/Archive.aspx?ADID=731",
            "url_hash": "02f4a611b6e0f1b6087196354955e11b",
            "category": "agenda"
        },
        {
            "url": "http://www.pbtech.org/clients/dublin_cc/dublinccm02072017.html",
            "url_hash": "02f4a611b6e0f1b6087196354955e11b",
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
**ocd_division_id:** Place's OCD division see table [here](https://github.com/Data4Democracy/town-council/blob/master/city_metadata/list_of_cities.csv). 
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

### Pipelines:
Read more about scrapy pipelines [here](https://doc.scrapy.org/en/latest/topics/item-pipeline.html)

**ValidateRecordDatePipeline:** Drop events if the `record_date` is not a valid python `datetime.date` object.

**CreateEventPipeline:**: Process events returned by the spiders and create a database record for each event if it does not exists. Requires database connection. This does not need to be activited (comment out to turn off) while developing spiders. Once a spider is fully developed the second step is to test it with a live database connection.  
**StageDocumentLinkPipeline:** Process document links returned by the spiders and stage link for downstream processing. Requires database connection. This does not need to be activited (comment out to turn off) while developing spiders. Once a spider is fully developed the second step is to test it with a live database connection.  


### Database Setup: & Exampl Usage
You can setup the required database & associated tables by running the `create_tables.py` script found in the `town-council/council_crawler`. When you run the script it will prompt you for the OCD_ID of the spider you are testing, this should be the full OCD_ID found in [here](https://github.com/Data4Democracy/town-council/blob/master/city_metadata/list_of_cities.csv) make sure this matches the value your spider is passing in the `ocd_division_id` field. ex `ocd-division/country:us/state:ca/place:belmont` (do not surround in quotes). 

Example useage
```
python create_tables.py
Enter OCD_ID of spider you wish to test: ocd-division/country:us/state:ca/place:belmont
```

Run your cralwer Ex: `scrapy crawl belmont` (Make sure you the `CreateEventPipeline'` & `'StageDocumentLinkPipeline' pipelines are active in the `settings.py` file)

Your spider output should be stored in the local database called `test_sqlite.sqlite` (if you used default settings)

To explore the data you can use the sqlite3 CLI by typing `sqlite3` hit enter then `.open test_sqlite.sqlite` (or whatever your db name is). If you prefer, there are many GUI options as well like this [firefox Add-On](https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/)


Check events
```
sqlite> select * from event limit 5;
1|1|Belmont, CA City Council Planning Commission Meeting|2017-06-14 11:01:43.571595|2017-12-19|belmont|http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all|Planning Commission Meeting
2|1|Belmont, CA City Council Planning Commission Meeting|2017-06-14 11:01:43.601113|2017-12-05|belmont|http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all|Planning Commission Meeting
3|1|Belmont, CA City Council Planning Commission Meeting|2017-06-14 11:01:43.619333|2017-11-21|belmont|http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all|Planning Commission Meeting
4|1|Belmont, CA City Council Planning Commission Meeting|2017-06-14 11:01:43.637540|2017-11-07|belmont|http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all|Planning Commission Meeting
5|1|Belmont, CA City Council Planning Commission Meeting|2017-06-14 11:01:43.655593|2017-10-17|belmont|http://www.belmont.gov/city-hall/city-government/city-meetings/-toggle-all|Planning Commission Meeting
```

Check document URLs
```
sqlite> select * from url_stage;
1|ocd-division/country:us/state:ca/place:belmont|Belmont, CA City Council City Council Meeting|2017-07-11|/city-hall/city-government/city-meetings/-toggle-all/-item-5065|d6c964939b81874a6fcb0dd19c9a2c8c|agenda|2017-06-14 07:01:43.834660
2|ocd-division/country:us/state:ca/place:belmont|Belmont, CA City Council City Council Meeting|2017-06-27|/city-hall/city-government/city-meetings/-toggle-all/-item-5057|0286667327ca256c459ee382349a3635|agenda|2017-06-14 07:01:43.882374
3|ocd-division/country:us/state:ca/place:belmont|Belmont, CA City Council City Council Special Meeting (Measure I Interviews)|2017-06-19|/city-hall/city-government/city-meetings/-toggle-all/-item-5063|7c818b339ff14752b8fed8150ec600fa|agenda|2017-06-14 07:01:43.929106
4|ocd-division/country:us/state:ca/place:belmont|Belmont, CA City Council City Council Meeting|2017-06-13|https://belmont-ca.granicus.com/GeneratedAgendaViewer.php?event_id=424|17bddda2de199e5c0ea7c3956bf206aa|agenda|2017-06-14 07:01:43.955555
5|ocd-division/country:us/state:ca/place:belmont|Belmont, CA City Council City Council Special Meeting (Closed Session)|2017-06-13|http://belmont-ca.granicus.com/GeneratedAgendaViewer.php?view_id=2&event_id=423|ef0331a277ef8cee0f6e8b2db6828fcf|agenda|2017-06-14 07:01:43.982026
6|ocd-division/country:us/state:ca/place:belmont|Belmont, CA City Council Parks and Recreation Commission Meeting|2017-06-07|http://belmont-ca.granicus.com/GeneratedAgendaViewer.php?event_id=8dfd98d2-464c-11e7-b343-f04da2064c47|5d2177d70cb1a4294fb36a7e642f85c0|agenda|2017-06-14 07:01:44.008042
```

Note: this process creates a database based on `STORAGE_ENGINE` value in `settings.py` (see below).

### Additional settings  

`STORAGE_ENGINE` is a sqlalchemy [database url](http://docs.sqlalchemy.org/en/latest/core/engines.html) used to create a database connection.

