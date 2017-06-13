from council_crawler import db_utils


def create_tables():
    engine, metadata = db_utils.setup_db()

    url_stage = db_utils.get_url_stage()
    place = db_utils.get_place()
    event = db_utils.get_event()

    url_stage.create()
    place.create()
    event.create()


if __name__ == '__main__':
    create_tables()
    engine, _ = db_utils.setup_db()
    ocd_id = input("Enter OCD_ID of spider you wish to test: ")
    place = db_utils.get_place()
    with engine.connect() as conn:
        conn.execute(
            place.insert(),
            ocd_division_id=str(ocd_id)
        )
