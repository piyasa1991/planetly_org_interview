import pytest
import sqlalchemy
import fastapi.testclient

import interview_app.models as models
import interview_app.core.config as settings
import interview_app.main as main
import interview_app.models as models
import interview_app.core.deps


@pytest.fixture(scope="session")
def engine():
    yield sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)


def seeded_database(session):
    return NotImplemented


@pytest.fixture(scope="session")
def connection(engine):
    connection = engine.connect()
    trans = connection.begin()
    yield connection
    import pdb

    pdb.set_trace()
    trans.rollback()
    connection.close()


@pytest.fixture
def db_session(connection):
    TestingSessionLocal = sqlalchemy.orm.sessionmaker()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        return db_session

    main.app.dependency_overrides[interview_app.core.deps.get_db] = override_get_db
    with fastapi.testclient.TestClient(main.app) as client:
        yield client
