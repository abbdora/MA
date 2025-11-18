import pytest
from unittest.mock import Mock, patch
from uuid import uuid4
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.models.user import User, UserCreate, UserLogin, Token


class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        mock_repo = Mock()
        with patch.object(AuthService, '__init__', lambda self, repo: setattr(self, 'user_repo', repo)):
            return AuthService(mock_repo)

    def test_password_hash_and_verify(self, auth_service):
        password = "test123"
        hashed = auth_service.get_password_hash(password)

        assert auth_service.verify_password(password, hashed)
        assert not auth_service.verify_password("wrong", hashed)

    def test_token_creation(self, auth_service):
        token = auth_service.create_access_token({"sub": "test@example.com"})
        assert token and isinstance(token, str)

    def test_user_registration(self, auth_service):
        auth_service.user_repo.create_user.return_value = User(
            id=uuid4(), email="test@example.com", username="testuser"
        )

        user_data = UserCreate(email="test@example.com", username="testuser", password="123")
        user = auth_service.register_user(user_data)

        assert user.email == "test@example.com"
        auth_service.user_repo.create_user.assert_called_once()

    def test_user_authentication(self, auth_service):
        mock_user = Mock()
        mock_user.id = uuid4()
        mock_user.email = "test@example.com"
        mock_user.username = "testuser"
        mock_user.hashed_password = auth_service.get_password_hash("correct")

        auth_service.user_repo.get_user_db_by_email.return_value = mock_user
        user = auth_service.authenticate_user("test@example.com", "correct")
        assert user is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"

        assert auth_service.authenticate_user("test@example.com", "wrong") is None

        auth_service.user_repo.get_user_db_by_email.return_value = None
        assert auth_service.authenticate_user("none@example.com", "123") is None

    def test_user_login(self, auth_service):
        mock_user = Mock()
        mock_user.id = uuid4()
        mock_user.email = "test@example.com"
        mock_user.username = "testuser"
        mock_user.hashed_password = auth_service.get_password_hash("123")

        auth_service.user_repo.get_user_db_by_email.return_value = mock_user

        token = auth_service.login_user(UserLogin(email="test@example.com", password="123"))
        assert isinstance(token, Token)
        assert token.token_type == "bearer"
        assert token.access_token is not None

        auth_service.user_repo.get_user_db_by_email.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            auth_service.login_user(UserLogin(email="test@example.com", password="123"))
        assert exc_info.value.status_code == 401