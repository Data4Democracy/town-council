import sqlite3

from scrapy.utils.project import get_project_settings

database = get_project_settings().get('DATABASE')


def save_url(item):
    """Save URL to specified database imported from DATABASE in
    settings.py"
    """

    if database['drivername'] == 'sqlite':
        # temporarily use SQLITE for prototyping & testing
        connection = sqlite3.connect(database['database'])
        cursor = connection.cursor()
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS URL_STAGE(
                    id INTEGER PRIMARY KEY,
                    event VARCHAR(80),
                    event_date DATE,
                    url VARCHAR(80),
                    media_type VARCHAR(80),
                    url_hash VARCHAR(80),
                    category VARCHAR(150),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                    )
                """
                )

        cursor.execute(
            """insert into URL_STAGE (
                event, event_date, url, media_type, url_hash, category) \
            values (?, ?, ?, ?, ?, ?)
            """,
            (item['event'],
             item['event_date'],
             item['url'],
             item['media_type'],
             item['url_hash'],
             item['category']))
        connection.commit()
    return item
