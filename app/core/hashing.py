from passlib.context import CryptContext
from typing import Callable


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


PasswordHasher = Callable[[str], str]
PasswordVerifier = Callable[[str, str], bool]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generates the hash of a plain password."""
    return pwd_context.hash(password)