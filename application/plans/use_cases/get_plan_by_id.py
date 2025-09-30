# application/plans/use_cases/get_plan_by_id.py
from dataclasses import dataclass
from typing import Optional
from brasiltransporta.domain.repositories.plan_repository import PlanRepository

@dataclass(frozen=True)
class GetPlanByIdOutput:
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
    features: list[str]
    created_at: str
    updated_at: str

class GetPlanByIdUseCase:
    def __init__(self, plans: PlanRepository):
        self._plans = plans

    def execute(self, plan_id: str) -> Optional[GetPlanByIdOutput]:
        plan = self._plans.get_by_id(plan_id)
        if not plan:
            return None
        
        return GetPlanByIdOutput(
            id=plan.id,
            name=plan.name,
            description=plan.description,
            plan_type=plan.plan_type.value,
            billing_cycle=plan.billing_cycle.value,
            price_amount=plan.price.amount,
            price_currency=plan.price.currency,
            max_ads=plan.max_ads,
            max_featured_ads=plan.max_featured_ads,
            is_active=plan.is_active,
            features=plan.features,
            created_at=plan.created_at.isoformat(),
            updated_at=plan.updated_at.isoformat()
        )
