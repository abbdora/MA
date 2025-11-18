from datetime import datetime, timedelta
from uuid import uuid4
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..models.user import User, UserCreate, UserLogin, Token
from ..repositories.db_user_repo import UserRepo
from ..database import get_db
from ..settings import settings

pwd_context = CryptContext(schemes=["sha256_crypt"])


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepo(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    def get_password_hash(self, password: str) -> str:
        if password is None:
            return ""

        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            password = password_bytes.decode('utf-8', errors='ignore')

        return pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    def register_user(self, user_data: UserCreate) -> User:
        hashed_password = self.get_password_hash(user_data.password)

        user_dict = {
            "id": uuid4(),
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password
        }

        return self.user_repo.create_user(user_dict)

    def authenticate_user(self, email: str, password: str) -> User:
        try:
            user_db = self.user_repo.get_user_db_by_email(email)
            if not user_db:
                return None

            if not self.verify_password(password, user_db.hashed_password):
                return None

            return User(
                id=user_db.id,
                email=user_db.email,
                username=user_db.username
            )
        except Exception:
            return None

    def login_user(self, login_data: UserLogin) -> Token:
        user = self.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token = self.create_access_token({"sub": user.email, "user_id": str(user.id)})
        return Token(access_token=access_token)

    def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        try:
            user = self.user_repo.get_user_by_email(email)
            return user
        except Exception:
            raise credentials_exception


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)