from fastapi import APIRouter, Depends, status
from app.schemas.chatbot import ChatbotRequest, ChatbotResponse
from app.services.chatbot import ChatbotService

router = APIRouter(tags=["Chatbot"])


def get_chatbot_service() -> ChatbotService:
    return ChatbotService()

@router.post("/", response_model=ChatbotResponse)
def ask_chatbot(
    query: ChatbotRequest,
    chatbot_service: ChatbotService = Depends(get_chatbot_service)
):
    """
    Endpoint that receives a user question and returns a predefined answer (chatbot simulation).
    """
    answer = chatbot_service.get_chatbot_response(query.question)
    return {"answer": answer}
