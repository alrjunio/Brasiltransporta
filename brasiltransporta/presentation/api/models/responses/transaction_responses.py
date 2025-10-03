# presentation/api/models/responses/transaction_responses.py
from pydantic import BaseModel
from typing import Optional, Dict

class CreateTransactionResponse(BaseModel):
    id: str

class TransactionDetailResponse(BaseModel):
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    external_payment_id: Optional[str]
    metadata: Dict
    created_at: str
    updated_at: str
