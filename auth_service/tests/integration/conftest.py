import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.user import Base

TEST_DB_URL = "postgresql+psycopg2://test_user:test_password@localhost/auth_test_db"


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        TEST_DB_URL,
        echo=True,
        pool_pre_ping=True,
        connect_args={
            'options': '-c client_encoding=utf8'
        }
    )

    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

    yield engine

    try:
        Base.metadata.drop_all(bind=engine)
        print("Tables dropped successfully")
    except Exception as e:
        print(f"Error dropping tables: {e}")

    engine.dispose()


@pytest.fixture()
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()


@pytest.fixture()
def user_repo(session):
    from app.repositories.db_user_repo import UserRepo
    return UserRepo(session)


@pytest.fixture()
def auth_service(session):
    from app.services.auth_service import AuthService
    return AuthService(session)