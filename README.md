# town-council

Tools to scrape and centralize the text of meeting agendas & minutes from local city governments.

**Slack:** [#p-town-council](http://datafordemocracy.slack.com/messages/p-town-council)

**Project Description:**
Engagement in local government is limited not only by physical access to city council meetings, but also electronic barriers including difficult-to-navigate web portals and the frequent use of scanned (non-text searchable) .pdf documents. That is, council meetings and their outcomes are not easily tracked by local constituents, journalists, and policy advocates.

Moreover, no tools exist to support the comparison of local government issues between cities.

We aim to provide a **publicly available database that automatically scrapes and aggregates the text from city council agendas and minutes**, towards the goals of: (1) promoting local government accessibility/transparency and (2) establishing open-source data/software resources to track and analyze trends in local governments.

## Project Status / Scope

**As of August 2017, this project is on hold -- new co-leads needed.** While the existing project members feel that this database is extremely valuable, we unfortunately don't have the time to maintain it at present. **We're currently looking for new leads interested in picking up the project.**

A rough draft of our infrastructure is shown [here](./design_doc.png). Stack: Python 3, [Scrapy 1.4](https://scrapy.org), postgresql.

We have completed scrapers for approximately a dozen cities in the San Francisco Bay Area as initial case study (selected in partnership with activists researching the Bay Area housing crisis; see [list of cities](./city_metadata/)), including some general scrapers that work with common content management systems used by cities (e.g., see our [Legistar scraper](./council_crawler/templates)).

We have also successfully automated the document retrieval process (i.e., downloading the agenda and minutes .pdf files; code in [pipeline](./pipeline/) folder).

Work-in-progress included investigating tools to extract the text from the said documents, as well as publicly setting up the database (AWS/Azure). Long-term goals include a front-end interface / search for users with less technical background.

## Contributing

**Project Co-Leads:**
[@chooliu](https://datafordemocracy.slack.com/messages/@chooliu/) / [@bstarling](https://datafordemocracy.slack.com/messages/@bstarling/) / TBD

_Again, this project is on hold due to limited availability of the current co-leads: please let us know if you'd like to help lead #p-town-council!_

To join, just post in the Slack channel ([#p-town-council](http://datafordemocracy.slack.com/messages/p-town-council)) or contact one of the leads following general [D4D onboarding](https://github.com/Data4Democracy/read-this-first).

For volunteers interested in writing scrapers/helping out with initial development, as a first step install , then try to run one of our scrapers using our "council crawler" [readme.md](./council_crawler/readme.md).

**Skills:**

Volunteers with backgrounds in and/or interest in learning the following are highly desired:

* web scraping
* .pdf scraping / OCR
* database management
* natural language processing / text wranglers

At present, our focus is to develop the database infrastructure (folks with web scraping experience highly desired!), but also welcome researchers/analysts interested in local politics and downstream analyses with the data.

Future analyses enabled with this database may include:

* Counting mentions of large organizations (lobbyist, think-tanks, corporations) in local meetings.
* Mapping concern for state/national issues (e.g., Affordable Health Care for America Act) at high resolution by pairing with local demographic metadata (e.g., political affiliation, median income).

## Related Work

While there are attempts to do this at the state and federal level (shoutout to organizations like [4US](https://4us.com/), [Digital Democracy](https://www.digitaldemocracy.org/), [GovTrack](https://www.govtrack.us/) and the [Open States Project](https://openstates.org/)), no similar resource yet exists for local governments.

However, we encourage those interested in learning more about local government / data science tools for civic tech to explore the great foundational work of [Open Civic Data](http://opencivicdata.readthedocs.io/en/latest/) and [Councilmatic](https://www.councilmatic.org/).
