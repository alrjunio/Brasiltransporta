from pydantic import BaseModel
from typing import Optional, List

class CreatePlanRequest(BaseModel):
    name: str
    description: Optional[str] = None
    plan_type: str            # aceita string; UC converte para enum
    billing_cycle: str
    price_amount: float
    price_currency: str = "BRL"
    max_ads: int = 10
    max_featured_ads: int = 1
    features: List[str] = []
