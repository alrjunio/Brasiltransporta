from typing import Optional
from pydantic import BaseModel

class CreateTransactionResponse(BaseModel):
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str = "BRL"
    payment_method: str
    status: str
    external_payment_id: Optional[str] = None

class TransactionDetailResponse(BaseModel):
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    external_payment_id: Optional[str] = None
