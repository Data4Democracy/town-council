
# town-council
Tools to scrape and centralize the text of meeting agendas & minutes from local city governments.

**Slack:** [#town-council](http://datafordemocracy.slack.com/messages/town-council)

**Project Description:**
Engagement in local government is limited not only by physical accessibility to city council meetings, but also difficult-to-navigate portals and frequent use of scanned .pdf documents (i.e., meeting issues and outcomes are not easily readable and searchable by constituents).

Moreover, no tools exist to support the comparison of local government issues between cities.

We aim to provide the infrastructure for a **publicly available database aggregating the text from city council agendas and minutes**, towards the goals of: (1) promoting local government accessibility/transparency and (2) establishing open-source data/software resources to track and analyze trends in local governments.

**Project Co-Leads:**
[@chooliu](https://datafordemocracy.slack.com/messages/@chooliu/) / [@bstarling](https://datafordemocracy.slack.com/messages/@bstarling/) / TBD (more leads needed!)

## Getting Started

To join, just post in the Slack channel or contact one of the leads following [D4D onboarding](https://github.com/Data4Democracy/read-this-first) or check out our Issues tab here on Github.

For volunteers interested in writing scrapers/helping out with initial development, as a first step install Python 3 & [Scrapy 1.4](https://scrapy.org), then try to run one of our scrapers using our "council crawler" [readme.md](./council_crawler/readme.md). 

**Skills:**

Volunteers with backgrounds in and/or interest in learning the following are highly desired:

* web scraping
* .pdf scraping / OCR
* database management
* natural language processing / text wranglers

At present, our focus is to develop the underlying scraping software/scripts for the database, but also welcome researchers/analysts interested in local politics and downstream analyses with the data.

Future analyses possible with our database may include:

* Counting mentions of large organizations (lobbyist, think-tanks, corporations) in local meetings.
* Mapping concern for state/national issues (e.g., Affordable Health Care for America Act) at high resolution by pairing with local demographic metadata (e.g., political affiliation, median income).

## Project Scope

Due to the high variation in how city council results are shared online from city-to-city (vastly different file infrastructures, minute/agenda formats & published information about each meeting), our central goal is to develop flexible, user-friendly scrapers that can be used with minimal user-modification, with the ultimate aim of scaling to scrape the text from as many cities' public agendas/meetings as possible.

We will maintain an up-to-date, public database of the text, alongside very fundamental meeting metadata (e.g., date, document URL, file format: detailed in [council crawler readme.md](https://github.com/Data4Democracy/town-council/tree/master/council_crawler#basic-structure)).

To begin, we've selected twenty-two cities in the San Francisco Bay Area as initial case study (see the [list of cities here](./city_metadata/)) to develop our system architecture. These cities were selected in partership with organizations researching the Bay Area housing crisis.

## Architecture
View very rough draft / 1st proposal [here](./design_doc.png).

As of June 2017, we're currently writing scrapers to identify meetings/agenda metadata and beginning to test the database locally (i.e., top/left side of design document). Next steps will be to develop the queue to process the documents. (Note: Some examples of city council documents for testing .pdf --> text tools are available at this public [Dropbox link](https://www.dropbox.com/sh/9bxu3ruvjsrir7o/AABg4uCiKczYK4gzD6OV_hbOa). This initial set of manually collected .pdfs will be updated soon with documents collected using the scrapers.)

After validating this architecture locally, we'll begin steps to deploy the database online (aiming for late summer 2017). Much later, we aim to develop a front-end interface for improving database access for users with less technical background.

## Related Work
* https://github.com/datamade/nyc-councilmatic (fully searchable council meetings and more for New York City)
* http://opencivicdata.readthedocs.io/en/latest/ (schemas for metadata on government entities -- used by #town-council when possible)
