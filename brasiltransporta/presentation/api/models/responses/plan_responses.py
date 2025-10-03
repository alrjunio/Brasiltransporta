# presentation/api/models/responses/plan_responses.py
from pydantic import BaseModel
from typing import List

class CreatePlanResponse(BaseModel):
    id: str

class PlanDetailResponse(BaseModel):
    id: str
    name: str
    description: str
    plan_type: str
    billing_cycle: str
    price_amount: float
    price_currency: str
    max_ads: int
    max_featured_ads: int
    is_active: bool
    features: List[str]
    created_at: str
    updated_at: str

class PlanListItem(BaseModel):
    id: str
    name: str
    description: str
    plan_type: str
    billing_cycle: str
    price_amount: float
    price_currency: str
    max_ads: int
    max_featured_ads: int
    features: List[str]

class ListPlansResponse(BaseModel):
    plans: List[PlanListItem]
from pydantic import BaseModel
from typing import List

class CreatePlanResponse(BaseModel):
    id: str

class PlanSummaryResponse(BaseModel):
    id: str
    name: str
    description: str
    plan_type: str
    billing_cycle: str
    price_amount: float
    price_currency: str
    max_ads: int
    max_featured_ads: int
    features: List[str]

class ListPlansResponse(BaseModel):
    plans: List[PlanSummaryResponse]
