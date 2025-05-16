import pytest
from fastapi.testclient import TestClient

from app.schemas.chatbot import ChatbotRequest, ChatbotResponse


def test_ask_chatbot_successful_keyword_balance(client: TestClient):
    """
    Testa se o chatbot responde corretamente a uma pergunta sobre saldo.
    """
    question_data = ChatbotRequest(question="Qual o meu saldo?")

    response = client.post(
        "/api/v1/chatbot/",
        json=question_data.model_dump()
    )

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "answer" in response_data
    assert isinstance(response_data["answer"], str)

    assert "saldo de transporte" in response_data["answer"]
    assert "api/v1/transport/balance" in response_data["answer"]


def test_ask_chatbot_successful_keyword_document(client: TestClient):
    """
    Testa se o chatbot responde corretamente a uma pergunta sobre documentos.
    """
    question_data = ChatbotRequest(question="Como eu vejo meus documentos?")

    response = client.post(
        "/api/v1/chatbot/",
        json=question_data.model_dump()
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "answer" in response_data
    assert isinstance(response_data["answer"], str)

    assert "documentos digitais" in response_data["answer"]
    assert "api/v1/documents" in response_data["answer"]


def test_ask_chatbot_successful_keyword_greeting(client: TestClient):
    """
    Testa se o chatbot responde corretamente a uma saudação.
    """
    question_data = ChatbotRequest(question="Olá, preciso de ajuda.")

    response = client.post(
        "/api/v1/chatbot/",
        json=question_data.model_dump()
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "answer" in response_data
    assert isinstance(response_data["answer"], str)

    assert "carteira digital municipal" in response_data["answer"]


def test_ask_chatbot_successful_no_keyword(client: TestClient):
    """
    Testa se o chatbot responde com a resposta padrão para perguntas sem palavras-chave conhecidas.
    """
    question_data = ChatbotRequest(question="Qual a capital da França?")

    response = client.post(
        "/api/v1/chatbot/",
        json=question_data.model_dump()
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "answer" in response_data
    assert isinstance(response_data["answer"], str)

    assert "Desculpe, não entendi sua pergunta" in response_data["answer"]


def test_ask_chatbot_invalid_input(client: TestClient):
    """
    Testa a tentativa de enviar uma requisição com dados inválidos (ex: sem o campo 'question').
    Deve retornar 422 Unprocessable Entity.
    """
    response = client.post(
        "/api/v1/chatbot/",
        json={}
    )

    assert response.status_code == 422
