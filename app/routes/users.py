from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User as UserResponseSchema

from app.dependencies import get_user_service_dependency
from app.services.user import UserService

router = APIRouter(tags=["Users"])


@router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service_dependency)
):
    new_user = user_service.create_user(user_data)
    return new_user
