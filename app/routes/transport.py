from fastapi import APIRouter, Depends, status
from app.schemas.transport import BalanceResponse, RechargeRequest
from app.schemas.user import User as UserSchema
from app.services.transport import TransportService
from app.core.security import get_current_user 


router = APIRouter(tags=["Transport"])


def get_transport_service() -> TransportService:
    return TransportService()

@router.get("/balance/", response_model=BalanceResponse)
def get_transport_balance(
    current_user: UserSchema = Depends(get_current_user),
    transport_service: TransportService = Depends(get_transport_service)
):
    """
    Endpoint para consultar saldo do passe de transporte (mockado) do usuário autenticado.
    """
    balance = transport_service.get_balance(current_user)
    return {"balance": balance}

@router.post("/recharge/", response_model=BalanceResponse)
def recharge_transport_balance(
    recharge_data: RechargeRequest,
    current_user: UserSchema = Depends(get_current_user),
    transport_service: TransportService = Depends(get_transport_service)
):
    """
    Endpoint para simular recarga do passe de transporte do usuário autenticado.
    """
    new_balance = transport_service.recharge_balance(current_user, recharge_data.amount)
    return {"balance": new_balance}
