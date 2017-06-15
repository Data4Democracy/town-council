from council_crawler import db_utils


def create_tables(metadata, engine):
    url_stage = db_utils.define_url_stage(metadata, engine)
    place = db_utils.define_place(metadata, engine)
    event = db_utils.define_event(metadata, engine)

    url_stage.create()
    place.create()
    event.create()


if __name__ == '__main__':
    engine, metadata = db_utils.setup_db()
    create_tables(metadata, engine)
    ocd_id = input("Enter OCD_ID of spider you wish to test: ")
    place = db_utils.new_get_place(metadata)
    with engine.connect() as conn:
        conn.execute(
            place.insert(),
            ocd_division_id=str(ocd_id)
        )
