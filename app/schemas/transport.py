from pydantic import BaseModel

class BalanceResponse(BaseModel):
    balance: float

class RechargeRequest(BaseModel):
    amount: float