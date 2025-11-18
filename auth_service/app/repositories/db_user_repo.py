from uuid import UUID
from sqlalchemy.orm import Session
from ..models.user import User  
from ..schemas.user import UserDB


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self) -> list[User]:
        users = []
        for user_db in self.db.query(UserDB).all():
            users.append(User.model_validate(user_db))
        return users

    def get_user_by_id(self, id: UUID) -> User:
        user_db = self.db.query(UserDB).filter(UserDB.id == id).first()
        if user_db is None:
            raise KeyError(f"User with id {id} not found")
        return User.model_validate(user_db)

    def get_user_by_email(self, email: str) -> User:
        user_db = self.db.query(UserDB).filter(UserDB.email == email).first()
        if user_db is None:
            raise KeyError(f"User with email {email} not found")
        return User.model_validate(user_db)

    def create_user(self, user_data: dict) -> User:
        existing_user = self.db.query(UserDB).filter(UserDB.email == user_data["email"]).first()
        if existing_user:
            raise ValueError("User with this email already exists")

        user_db = UserDB(**user_data)
        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)
        return User.model_validate(user_db)

    def get_user_db_by_email(self, email: str) -> UserDB:
        user_db = self.db.query(UserDB).filter(UserDB.email == email).first()
        if user_db is None:
            raise KeyError(f"User with email {email} not found")
        return user_db