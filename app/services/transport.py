from typing import Dict
from app.schemas.user import User as UserSchema
from fastapi import HTTPException, status

mock_balances: Dict[int, float] = {}

class TransportService:
    def get_balance(self, current_user: UserSchema) -> float:
        """Consulta saldo do usuário (mockado)."""
        return mock_balances.get(current_user.id, 0.0)

    def recharge_balance(self, current_user: UserSchema, amount: float) -> float:
        """Simula recarga de saldo do usuário (mockado)."""
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor de recarga deve ser positivo"
            )

        current_balance = mock_balances.get(current_user.id, 0.0)
        new_balance = current_balance + amount
        mock_balances[current_user.id] = new_balance

        return new_balance
