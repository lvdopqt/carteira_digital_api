import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User as UserResponseSchema
from app.models.user import User as UserModel
from app.core.security import verify_password

def test_create_user_successful(client: TestClient, db: Session):
    """
    Test creating a new user successfully via the API endpoint.
    """
    # Define the data for the new user
    user_data = UserCreate(
        email="newuser@example.com",
        password="securepassword123",
        full_name="New Test User",
        is_active=True,
        is_superuser=False,
    )

    # Send a POST request to the user creation endpoint
    # Ensure the URL matches how you included the users router (e.g., /api/v1/users/)
    response = client.post("/api/v1/users/", json=user_data.model_dump()) # Use model_dump() for Pydantic v2+

    # Assert the response status code is 201 Created
    assert response.status_code == 201

    # Parse the JSON response
    response_data = response.json()

    # Assert the response matches the expected UserResponseSchema structure and data
    # Check basic fields returned by the API
    assert "id" in response_data
    assert isinstance(response_data["id"], int)
    assert response_data["email"] == user_data.email
    assert response_data["full_name"] == user_data.full_name
    assert response_data["is_active"] == user_data.is_active
    assert response_data["is_superuser"] == user_data.is_superuser

    # Verify the user was actually created in the database
    # Query the database directly using the 'db' fixture
    created_user_in_db = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    # Assert the user exists in the DB
    assert created_user_in_db is not None
    assert created_user_in_db.email == user_data.email
    assert created_user_in_db.full_name == user_data.full_name
    assert created_user_in_db.is_active == user_data.is_active
    assert created_user_in_db.is_superuser == user_data.is_superuser

    # Verify the password was hashed correctly (by checking if the plain password matches the hash)
    assert verify_password(user_data.password, created_user_in_db.hashed_password)


def test_create_user_duplicate_email(client: TestClient, db: Session):
    """
    Test attempting to create a user with an email that already exists.
    Should return a 400 Bad Request error.
    """
    # First, create a user directly in the database using the db fixture
    # This user will already exist when the API endpoint is called
    existing_email = "existinguser@example.com"
    hashed_password = "somehashedpassword" # Doesn't need to be a real hash for this test
    existing_user = UserModel(email=existing_email, hashed_password=hashed_password)
    db.add(existing_user)
    db.commit() # Commit to make the user exist in the DB session used by the API

    # Define data for a new user with the same email
    duplicate_user_data = UserCreate(
        email=existing_email,
        password="anotherpassword",
        full_name="Duplicate User",
    )

    # Send a POST request to the user creation endpoint with the duplicate email
    response = client.post("/api/v1/users/", json=duplicate_user_data.model_dump())

    # Assert the response status code is 400 Bad Request
    assert response.status_code == 400

    # Optional: Assert the error detail message
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Email already registered"

    # Verify that no new user was created with this email (should still be only the original one)
    users_with_email = db.query(UserModel).filter(UserModel.email == existing_email).all()
    assert len(users_with_email) == 1 # Only the initially created user should exist
