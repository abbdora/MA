import pytest
from uuid import uuid4
from pydantic import ValidationError

# Правильные импорты
from app.models.user import User, UserCreate, UserLogin, Token

class TestUserModels:
    def test_user_creation_valid(self):
        user_id = uuid4()
        user = User(
            id=user_id,
            email="test@example.com",
            username="testuser"
        )
        assert user.id == user_id
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    def test_user_create_valid(self):
        user_data = UserCreate(
            email="valid@example.com",
            username="validuser",
            password="password123"
        )
        assert user_data.email == "valid@example.com"
        assert user_data.username == "validuser"
        assert user_data.password == "password123"