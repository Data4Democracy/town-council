
# town-council
Tools to scrape and centralize the text of meeting agendas & minutes from local city governments.

**Slack:** [#town-council](http://datafordemocracy.slack.com/messages/town-council)

**Project Description:**
Access to city council meetings can be limited not only physically, but even electronically due user-unfriendly web navigation portals and frequent use of scanned .pdf documents (i.e., meeting issues and outcomes not easily readable and searchable). Moreover, no tools exist to compare local government issues between cities.

We aim to provide the infrastructure for a **publicly available, text-searchable database aggregating city council agendas and minutes**, towards the goals of: (1) promoting local government accessibility/transparency and (2) establishing open-source data/software resources to track and analyze trends in local governments.

**Project Co-Leads:**
[@chooliu](https://datafordemocracy.slack.com/messages/@chooliu/) / TBD (more leads needed!)

## Getting Started

To join, just say hi in Slack after general [D4D onboarding](https://github.com/Data4Democracy/read-this-first) or check out our Issues tab on Github.

**Skills:**

Volunteers with backgrounds in and/or interest in learning the following are highly desired:

* web & .pdf scraping
* database management
* natural language processing / text wranglers

At present, our focus is to develop the underlying scraping software/scripts for the database, but also welcome researchers/analysts interested in local politics and downstream analyses with the data. Possible later analyses might include:

* Counting mentions of large organizations (lobbyist, think-tanks, corporations) in local meetings.
* Mapping concern for state/national issues (e.g., Affordable Health Care for America Act) at high resolution by pairing with local demographic metadata (e.g., political affiliation, median income).

## Project Scope:

Given the high variation in how city council results are shared online from city-to-city (different file infrastructures, minute/agenda formats), our **initial focus** is to develop flexible, user-friendly tools that can be used with little modification to scrape different cities' public agendas/meetings.

This project is extremely new (founded late April 2017). To begin tool/database development, we've selected twenty-two cities in the San Francisco Bay Area as initial case studies. Initial scrapers will developed in Python/[Scrapy](https://scrapy.org).

To see the list of cities / update city information like location of meetings, refer to the [city metadata](https://github.com/Data4Democracy/town-council/tree/master/city_metadata) folder hosted on this repo.

Examples of city council documents for testing .pdf scraping tools are available at this public [Dropbox link](http://www.dropbox.com/sh/9bxu3ruvjsrir7o/AABg4uCiKczYK4gzD6OV_hbOa?dl=0).

## Architecture
* View very rough draft 1st proposal [here](./design_doc.png)

## Scrapy
* Read more [here](./council_crawler/readme.md)
