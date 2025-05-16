from fastapi import FastAPI
from app.api.api import api_router

from app.routes.health import router as health_router

app = FastAPI(title="Carteira Digital API")

app.include_router(api_router)

app.include_router(health_router)
