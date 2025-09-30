# application/plans/use_cases/list_active_plans.py
from dataclasses import dataclass
from typing import List
from brasiltransporta.domain.repositories.plan_repository import PlanRepository

@dataclass(frozen=True)
class PlanListItem:
    id: str
    name: str
    description: str
    plan_type: str
    billing_cycle: str
    price_amount: float
    price_currency: str
    max_ads: int
    max_featured_ads: int
    features: list[str]

@dataclass(frozen=True)
class ListActivePlansOutput:
    plans: List[PlanListItem]

class ListActivePlansUseCase:
    def __init__(self, plans: PlanRepository):
        self._plans = plans

    def execute(self) -> ListActivePlansOutput:
        active_plans = self._plans.list_active()
        
        plan_items = [
            PlanListItem(
                id=plan.id,
                name=plan.name,
                description=plan.description,
                plan_type=plan.plan_type.value,
                billing_cycle=plan.billing_cycle.value,
                price_amount=plan.price.amount,
                price_currency=plan.price.currency,
                max_ads=plan.max_ads,
                max_featured_ads=plan.max_featured_ads,
                features=plan.features
            )
            for plan in active_plans
        ]
        
        return ListActivePlansOutput(plans=plan_items)
