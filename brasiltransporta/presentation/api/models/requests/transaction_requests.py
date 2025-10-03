from pydantic import BaseModel
from typing import Optional, Dict

class CreateTransactionRequest(BaseModel):
    user_id: str
    plan_id: str
    amount: float
    payment_method: str  # aceitar "credit_card" literal dos testes
    currency: str = "BRL"
    metadata: Optional[Dict] = None
