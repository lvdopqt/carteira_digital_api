import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User as UserResponseSchema
from app.models.user import User as UserModel
from app.core.hashing import verify_password # Import verify_password

def test_create_user_successful(client: TestClient, db: Session): # Added db: Session dependency back for verification
    """
    Test creating a new user successfully via the API endpoint.
    """
    user_data = UserCreate(
        email="newuser@example.com",
        password="securepassword123",
        full_name="New Test User",
        is_active=True,
        is_superuser=False,
    )

    response = client.post("/api/v1/users/", json=user_data.model_dump())

    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert isinstance(response_data["id"], int)
    assert response_data["email"] == user_data.email
    assert response_data["full_name"] == user_data.full_name
    assert response_data["is_active"] == user_data.is_active
    assert response_data["is_superuser"] == user_data.is_superuser

    # Direct DB verification using the db fixture
    created_user_in_db = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    # Assert the user exists in the DB
    assert created_user_in_db is not None
    assert created_user_in_db.email == user_data.email
    assert created_user_in_db.full_name == user_data.full_name
    assert created_user_in_db.is_active == user_data.is_active
    assert created_user_in_db.is_superuser == user_data.is_superuser

    # Verify the password was hashed correctly
    assert verify_password(user_data.password, created_user_in_db.hashed_password)


def test_create_user_duplicate_email(client: TestClient, db: Session): # Keep db: Session for pre-populating DB
    """
    Test attempting to create a user with an email that already exists.
    Should return a 400 Bad Request error.
    """
    # This test *needs* the db fixture to pre-populate the database
    existing_email = "existinguser@example.com"
    hashed_password = "somehashedpassword" # Doesn't need to be a real hash for this test
    existing_user = UserModel(email=existing_email, hashed_password=hashed_password)
    db.add(existing_user)
    # REMOVE the explicit commit here, the 'db' fixture handles the transaction
    # db.commit()
    db.flush() # Use flush to ensure the object is in the session

    duplicate_user_data = UserCreate(
        email=existing_email,
        password="anotherpassword",
        full_name="Duplicate User",
    )

    response = client.post("/api/v1/users/", json=duplicate_user_data.model_dump())

    assert response.status_code == 400

    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Email already registered"

    # This assertion also needs the db fixture
    users_with_email = db.query(UserModel).filter(UserModel.email == existing_email).all()
    assert len(users_with_email) == 1 # Only the initially created user should exist
