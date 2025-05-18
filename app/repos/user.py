from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.user import User as UserModel
from app.schemas.user import UserCreate

class UserRepository:
    """
    Repository responsible for direct interaction with the 'users' table in the database.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> UserModel | None:
        """Finds a user by email."""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, user_id: int) -> UserModel | None:
        """Finds a user by ID."""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def create(self, user_data: UserCreate, hashed_password: str) -> UserModel:
        """Creates a new user in the database."""
        db_user = UserModel(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def find_or_create_oauth_user(self, email: str, full_name: Optional[str] = None, hashed_placeholder_password: str = "placeholder") -> UserModel:
        """
        Finds a user by email or creates a new one for OAuth login.
        Note: The placeholder password hash should be generated BEFORE calling this method.
        """
        user = self.get_by_email(email)

        if user is None:
            # User doesn't exist, create a new one
            db_user = UserModel(
                email=email,
                hashed_password=hashed_placeholder_password,
                full_name=full_name,
                is_active=True,
                is_superuser=False,
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            user = db_user

        return user
