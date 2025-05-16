import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.transport import BalanceResponse, RechargeRequest
from app.models.user import User as UserModel


def test_get_transport_balance_successful(client: TestClient, user_auth_token: str, reset_transport_balances):
    """
    Testa a consulta de saldo do transporte para um usuário autenticado.
    O saldo inicial deve ser 0.0, pois a lógica é mockada em memória por teste.
    """
    
    response = client.get(
        "/api/v1/transport/balance/",
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "balance" in response_data
    assert isinstance(response_data["balance"], (int, float))

    assert response_data["balance"] == 0.0


def test_get_transport_balance_unauthorized(client: TestClient):
    """
    Testa a tentativa de consultar saldo sem autenticação.
    Deve retornar 401 Unauthorized.
    """
    response = client.get("/api/v1/transport/balance/")

    assert response.status_code == 401


def test_recharge_transport_balance_successful(client: TestClient, user_auth_token: str, reset_transport_balances):
    """
    Testa a simulação de recarga de saldo do transporte para um usuário autenticado.
    """
    
    recharge_data = RechargeRequest(amount=50.75)

    response = client.post(
        "/api/v1/transport/recharge/",
        json=recharge_data.model_dump(),
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "balance" in response_data
    assert isinstance(response_data["balance"], (int, float))

    assert response_data["balance"] == recharge_data.amount


def test_recharge_transport_balance_unauthorized(client: TestClient):
    """
    Testa a tentativa de recarregar saldo sem autenticação.
    Deve retornar 401 Unauthorized.
    """
    recharge_data = RechargeRequest(amount=30.00)

    response = client.post(
        "/api/v1/transport/recharge/",
        json=recharge_data.model_dump()
    )

    assert response.status_code == 401

def test_recharge_transport_balance_invalid_amount(client: TestClient, user_auth_token: str, reset_transport_balances):
    """
    Testa a tentativa de recarregar saldo com um valor inválido (zero ou negativo).
    Deve retornar 400 Bad Request.
    """
    
    recharge_data_zero = RechargeRequest(amount=0.0)
    recharge_data_negative = RechargeRequest(amount=-10.0)

    # Testa com valor zero
    response_zero = client.post(
        "/api/v1/transport/recharge/",
        json=recharge_data_zero.model_dump(),
        headers={"Authorization": user_auth_token}
    )
    assert response_zero.status_code == 400
    assert "detail" in response_zero.json()

    # Testa com valor negativo
    response_negative = client.post(
        "/api/v1/transport/recharge/",
        json=recharge_data_negative.model_dump(),
        headers={"Authorization": user_auth_token}
    )
    assert response_negative.status_code == 400
    assert "detail" in response_negative.json()


def test_recharge_and_get_balance(client: TestClient, user_auth_token: str, reset_transport_balances):
    """
    Testa a recarga e depois consulta o saldo para verificar se foi atualizado.
    """
    
    response_initial = client.get(
        "/api/v1/transport/balance/",
        headers={"Authorization": user_auth_token}
    )
    assert response_initial.status_code == 200
    assert response_initial.json()["balance"] == 0.0

    
    recharge_amount = 100.50
    recharge_data = RechargeRequest(amount=recharge_amount)
    response_recharge = client.post(
        "/api/v1/transport/recharge/",
        json=recharge_data.model_dump(),
        headers={"Authorization": user_auth_token}
    )
    assert response_recharge.status_code == 200
    assert response_recharge.json()["balance"] == recharge_amount

    response_final = client.get(
        "/api/v1/transport/balance/",
        headers={"Authorization": user_auth_token}
    )
    assert response_final.status_code == 200
    assert response_final.json()["balance"] == recharge_amount

