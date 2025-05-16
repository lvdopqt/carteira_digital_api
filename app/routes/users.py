from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User as UserResponseSchema
from app.services.user import UserService
from app.db.session import get_db

router = APIRouter(tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user.
    """
    new_user = user_service.create_user(user_data)
    return new_user
