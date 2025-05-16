from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import Token, LoginRequest
from app.services.auth import login_user
from app.db.session import get_db

router = APIRouter()

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(data.email, data.password, db)