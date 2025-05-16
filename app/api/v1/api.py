from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.documents import router as documents_router
from app.routes.transport import router as transport_router
from app.routes.chatbot import router as chatbot_router

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(auth_router, prefix="/auth")
api_v1_router.include_router(users_router, prefix="/users")
api_v1_router.include_router(documents_router, prefix="/documents")
api_v1_router.include_router(transport_router, prefix="/transport")
api_v1_router.include_router(chatbot_router, prefix="/chatbot")