from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db 
from app.services.user import UserService

def get_user_service_dependency(
    db: Session = Depends(get_db),
) -> UserService:
    """Dependency that provides a UserService instance."""
    return UserService(db)
