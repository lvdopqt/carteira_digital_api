
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.schemas.user import Token, LoginRequest
from app.models.user import User as UserModel


def test_login_successful(client: TestClient, test_user: UserModel):
    """Testa se o login com credenciais corretas funciona."""
    login_data = LoginRequest(email=test_user.email, password="testpassword")
    response = client.post("/api/v1/auth/login", json=login_data.model_dump()) 
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client: TestClient, test_user: UserModel):
    """Testa se o login falha com senha incorreta."""
    login_data = LoginRequest(email=test_user.email, password="wrongpassword")
    response = client.post("/api/v1/auth/login", json=login_data.model_dump())

    assert response.status_code == 401

def test_login_user_not_found(client: TestClient):
    """Testa se o login falha com e-mail não registrado."""
    login_data = LoginRequest(email="nonexistent@example.com", password="somepassword")
    response = client.post("/api/v1/auth/login", json=login_data.model_dump())

    assert response.status_code == 401