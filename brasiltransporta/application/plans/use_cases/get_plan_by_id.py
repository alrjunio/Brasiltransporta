from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from brasiltransporta.domain.repositories.plan_repository import PlanRepository

@dataclass(frozen=True)
class PlanDetailOutput:
    id: str
    name: str
    description: str | None
    plan_type: str
    billing_cycle: str
    price_amount: float
    price_currency: str
    max_ads: int
    max_featured_ads: int
    is_active: bool
    features: list[str]
    created_at: datetime
    updated_at: datetime | None

def _enum_to_str(v: Any) -> str:
    return getattr(v, "value", str(v))

def _to_float(v: Any) -> float:
    # aceita Decimal, int, float
    try:
        return float(v)
    except Exception:
        return 0.0

class GetPlanByIdUseCase:
    def __init__(self, plans: PlanRepository) -> None:
        self._plans = plans

    def execute(self, plan_id: str) -> Optional[PlanDetailOutput]:
        p = self._plans.get_by_id(plan_id)
        if p is None:
            return None
        return PlanDetailOutput(
            id=str(p.id),
            name=p.name,
            description=getattr(p, "description", None),
            plan_type=_enum_to_str(getattr(p, "plan_type", "")),
            billing_cycle=_enum_to_str(getattr(p, "billing_cycle", "")),
            price_amount=_to_float(getattr(p, "price_amount", 0)),
            price_currency=str(getattr(p, "price_currency", "BRL")),
            max_ads=int(getattr(p, "max_ads", 0)),
            max_featured_ads=int(getattr(p, "max_featured_ads", 0)),
            is_active=bool(getattr(p, "is_active", True)),
            features=list(getattr(p, "features", []) or []),
            created_at=getattr(p, "created_at"),
            updated_at=getattr(p, "updated_at", None),
        )
