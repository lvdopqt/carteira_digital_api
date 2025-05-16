from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Any, Union

from app.core.config import settings
from app.db.session import get_db
from app.dependencies import get_user_service_dependency

from app.services.user import UserService
from app.schemas.user import User as UserSchema
from app.models.user import User as UserModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Union[dict[str, Any], None]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

class GetCurrentUser:
    def __init__(self, oauth_scheme: OAuth2PasswordBearer = Depends(oauth2_scheme)):
        self.oauth_scheme = oauth_scheme

    def __call__(self,
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service_dependency)
    ) -> UserSchema:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        try:
            user_orm = user_service.get_user_by_id(int(user_id))
        except Exception:
             raise credentials_exception


        if user_orm is None:
            raise credentials_exception

        return UserSchema.model_validate(user_orm)

get_current_user = GetCurrentUser()
