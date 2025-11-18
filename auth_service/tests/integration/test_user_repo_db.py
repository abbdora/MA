import pytest
from uuid import uuid4
from app.models.user import User
from app.repositories.db_user_repo import UserRepo
from app.schemas.user import UserDB

class TestUserRepoIntegration:
    """Интеграционные тесты репозитория пользователей с реальной PostgreSQL БД"""

    @pytest.fixture
    def user_repo(self, session):
        return UserRepo(session)

    def test_create_and_retrieve_user(self, user_repo):
        """Обязательный: создание и основные операции поиска пользователя"""
        user_data = {
            "id": str(uuid4()),
            "email": "test@example.com",
            "username": "testuser",
            "hashed_password": "hashed_password_123"
        }

        # Создание пользователя
        user = user_repo.create_user(user_data)
        assert user.email == "test@example.com"
        assert str(user.id) == user_data["id"]

        # Поиск по ID и email
        assert user_repo.get_user_by_id(user_data["id"]).email == "test@example.com"
        assert user_repo.get_user_by_email("test@example.com").username == "testuser"

    def test_email_uniqueness(self, user_repo):
        """Обязательный: проверка уникальности email"""
        user_data = {
            "id": str(uuid4()),
            "email": "unique@example.com",
            "username": "user1",
            "hashed_password": "hash1"
        }

        user_repo.create_user(user_data)

        # Попытка создать пользователя с тем же email
        with pytest.raises(ValueError):
            user_repo.create_user({
                "id": str(uuid4()),
                "email": "unique@example.com",
                "username": "user2",
                "hashed_password": "hash2"
            })

    def test_error_handling(self, user_repo):
        """Обязательный: обработка ошибок для несуществующих записей"""
        with pytest.raises(KeyError):
            user_repo.get_user_by_id(str(uuid4()))

        with pytest.raises(KeyError):
            user_repo.get_user_by_email("nonexistent@example.com")