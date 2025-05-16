import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator, Any

from app.main import app
from app.db.base_class import Base
from app.models.user import User
from app.models.document import Document
from app.core.hashing import get_password_hash

from app.models.user import User as UserModel

# Import the mock_balances dictionary from the transport service
from app.services.transport import mock_balances

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(scope="function")
def db(db_engine) -> Generator[Session, Any, None]:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    from app.db.session import get_db
    app.dependency_overrides[get_db] = lambda: session

    yield session

    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db: Session):
    email = "testuser@example.com"
    password = "testpassword"
    hashed_password = get_password_hash(password)

    user = User(email=email, hashed_password=hashed_password, is_active=True, is_superuser=False, full_name="Test User")
    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def user_auth_token(client: TestClient, test_user: UserModel):
    login_data = {"email": test_user.email, "password": "testpassword"}

    response = client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 200, f"Expected status 200, but got {response.status_code}. Response: {response.text}"

    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    return f"Bearer {token_data['access_token']}"

@pytest.fixture(scope="function")
def reset_transport_balances():
    mock_balances.clear()
    yield
