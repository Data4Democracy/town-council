## city_metadata

The city_metadata folder currently contains city metadata for the pilot cities (twenty Bay Area municipalities)
used to develop the round of scraping infrastructure.

These cities were manually curated by the project maintainers / project partners, but in the future we envision users
submitting their own municipalities of interest / scrapers for addition to the database.

## fields

The metadata collected on each city is limited at present:
in practice other fields aren't necesary for our web/document scraping infrastructure at present.

We may consider more detailed fields (developed in accordance with [Open Civic Data](http://opencivicdata.readthedocs.io/en/latest/)
standards in the future with more manpower + interest. (let us know if there's anything else you'd like to see here!)

* `city` : name of city/municipality.
* `state` : state or territory postal abbreviation.
* `country` : limited to the united states (US) for now.
* `display_name` : to be used for scraper names (join `city` and `state`, replace punctation and spaces with underlines).
* `ocd_division_id` : Open Civic Data division identifier. see comments in [issue #4](https://github.com/Data4Democracy/town-council/issues/4) for tools to make sure that these are in the correct format. currently not being collected beyond the city ("place") resolution.
* `city_council_url` : URL to where agendas and meetings can be found for the city. (note: some cities have distinct archive pages for each year; these link to the most recent year / most recent postings for now)
* `hosting_services` : this field's intent is to catalgoue cities that use legislative platform services (namely, Granicus, Legistar, and SIRE)
    * we may eventually attempt to write general scrapers that target these (somewhat standardized) hosting services.
    * documents hosted by Google Docs, AWS are also noted because they may cause redirect issues (currently being troubleshooted).
