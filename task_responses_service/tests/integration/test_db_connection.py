import pytest
from sqlalchemy import create_engine, text


def test_database_connection():
    """Проверка подключения к тестовой БД"""
    TEST_DB_URL = "postgresql+psycopg2://test_user:test_password@localhost/responses_test_db"

    try:
        engine = create_engine(TEST_DB_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        print("✅ Database connection successful!")
    except Exception as e:
        pytest.fail(f"❌ Database connection failed: {e}")