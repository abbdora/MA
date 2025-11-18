import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base_schema import Base

# Используем PostgreSQL как в auth_service
TEST_DB_URL = "postgresql+psycopg2://test_user:test_password@localhost/responses_test_db"

@pytest.fixture(scope='session')
def engine():
    """Двигатель БД для всех интеграционных тестов"""
    engine = create_engine(
        TEST_DB_URL,
        echo=True,
        pool_pre_ping=True,
        connect_args={
            'options': '-c client_encoding=utf8'
        }
    )

    try:
        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

    yield engine

    # Очищаем после всех тестов
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped successfully")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")

    engine.dispose()

@pytest.fixture()
def session(engine):
    """Сессия БД для каждого теста"""
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Откатываем изменения после каждого теста
    session.rollback()
    session.close()

@pytest.fixture()
def response_repo(session):
    """Репозиторий ответов для тестов"""
    from app.repositories.response_repo import ResponseRepository
    return ResponseRepository(session)