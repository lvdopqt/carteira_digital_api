from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Callable

from app.db.session import get_db
# Importe o UserRepository e o UserService
from app.repos.user import UserRepository
from app.services.user import UserService

def get_user_repository_dependency(db: Session = Depends(get_db)) -> UserRepository:
    """Dependência que fornece uma instância de UserRepository."""
    return UserRepository(db)

def get_user_service_dependency( 
    user_repo: UserRepository = Depends(get_user_repository_dependency),
) -> UserService:
    """Dependência que fornece uma instância de UserService com UserRepository injetado."""
    return UserService(user_repo)

