import pytest
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select
import buddy.db as sut

IN_MEMORY_SQLITE_CONN_STR = "sqlite:///:memory:"
LOCAL_SQLITE_FILE = "test_output/test-buddy-db.db"
LOCAL_SQLITE_CONN_STR = f"sqlite:///{LOCAL_SQLITE_FILE}"

# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test
@pytest.fixture(autouse=True, scope="module")
def get_db_objects():
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    engine: Engine = sqlalchemy.create_engine(LOCAL_SQLITE_CONN_STR)
    sut.drop_tables(engine)
    sut.create_tables(engine)

    print("set up DB engine!")
    yield (engine, None)  # this is where the testing happens

    # Teardown : fill with any logic you want
    print("Teardown after all tests!")
    sut.drop_tables(engine)
    engine.dispose()

def test_hello_world(get_db_objects):
    engine, _ = get_db_objects

    with Session(engine) as session:
        session.add(
            sut.TeamConfig(
                client_id="abcdefg4",
                team_id="T0112334"
            )
        )
        session.commit()

        # TODO: how to add event config tied to a team?
        stmt = select(sut.TeamConfig).where(sut.TeamConfig.client_id == "abcdefg4")

        first_row = session.scalars(stmt).one()
        print('Fr', first_row)

        session.add(sut.EventConfig(
            team_config_id=first_row.id,
            event_type="app_mention",
            desc="Proxying values on the way",
            webhook_url="https://webhook.url",
            creator="UMTUPT124"
        ))
        session.commit()

        stmt = select(sut.TeamConfig)

        for tc in session.scalars(stmt):
            print('TC', tc.event_configs)


