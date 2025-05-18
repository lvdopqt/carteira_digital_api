from sqlalchemy.orm import Session
from typing import Optional, Callable
from fastapi import HTTPException, status

from app.repos.user import UserRepository
from app.schemas.user import UserCreate, User as UserSchema
from app.models.user import User as UserModel
from app.core.hashing import get_password_hash, verify_password

class UserService:
    """
    Service responsible for user-related business logic.
    Uses the UserRepository to interact with the database.
    """
    def __init__(self, user_repo: UserRepository): 
        self.user_repo = user_repo
        
    def get_user_by_email(self, email: str) -> UserModel | None:
        return self.user_repo.get_by_email(email)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        return self.user_repo.get_by_id(user_id)

    def create_user(self, user_data: UserCreate) -> UserModel:
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = get_password_hash(user_data.password) 
        return self.user_repo.create(user_data, hashed_password)

    
    def find_or_create_oauth_user(self, email: str, full_name: Optional[str] = None) -> UserModel:
        """
        Finds a user by email or creates a new one if not found, via repository.
        """
        placeholder_password_hash = get_password_hash("oauth-placeholder-password-very-long-and-random-" + email)
        return self.user_repo.find_or_create_oauth_user(
            email=email,
            full_name=full_name,
            hashed_placeholder_password=placeholder_password_hash 
        )
    
    def authenticate_user(self, email: str, password: str) -> UserModel | None:
        user = self.user_repo.get_by_email(email) 
        if not user or not verify_password(password, user.hashed_password): 
            return None
        return user
