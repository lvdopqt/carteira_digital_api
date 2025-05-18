from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.user import User as UserModel # Import the User ORM model
from app.schemas.user import UserCreate # Import the creation schema

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
            hashed_password=hashed_password, # Receives the already hashed password from the service
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    # Add methods for find_or_create_oauth_user, update, delete, etc., if needed
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
                hashed_password=hashed_placeholder_password, # Uses the provided placeholder hash
                full_name=full_name,
                is_active=True,
                is_superuser=False,
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            user = db_user

        return user
