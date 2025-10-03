from dataclasses import dataclass
from typing import List, Any

from brasiltransporta.domain.repositories.plan_repository import PlanRepository
from brasiltransporta.application.plans.use_cases.get_plan_by_id import PlanDetailOutput, _enum_to_str, _to_float

@dataclass(frozen=True)
class PlanListItemOutput:
    id: str
    name: str
    description: str | None
    plan_type: str
    billing_cycle: str
    price_amount: float
    price_currency: str
    max_ads: int
    max_featured_ads: int
    features: list[str]

@dataclass(frozen=True)
class ListActivePlansOutput:
    plans: List[PlanListItemOutput]

def _map_item(p: Any) -> PlanListItemOutput:
    return PlanListItemOutput(
        id=str(p.id),
        name=p.name,
        description=getattr(p, "description", None),
        plan_type=_enum_to_str(getattr(p, "plan_type", "")),
        billing_cycle=_enum_to_str(getattr(p, "billing_cycle", "")),
        price_amount=_to_float(getattr(p, "price_amount", 0)),
        price_currency=str(getattr(p, "price_currency", "BRL")),
        max_ads=int(getattr(p, "max_ads", 0)),
        max_featured_ads=int(getattr(p, "max_featured_ads", 0)),
        features=list(getattr(p, "features", []) or []),
    )

class ListActivePlansUseCase:
    """
    Primeiro tenta usar PlanRepository.list_active(); se não existir,
    faz um fallback via list_all() e filtra por is_active/status.
    """
    def __init__(self, plans: PlanRepository) -> None:
        self._plans = plans

    def execute(self) -> ListActivePlansOutput:
        plans = None
        if hasattr(self._plans, "list_active"):
            try:
                plans = self._plans.list_active()
            except Exception:
                plans = None
        if plans is None:
            # fallback: se o repo não tiver list_active
            if hasattr(self._plans, "list_all"):
                all_plans = self._plans.list_all()  # type: ignore
            else:
                raise RuntimeError("PlanRepository precisa expor list_active() ou list_all().")
            plans = [
                p for p in all_plans
                if bool(getattr(p, "is_active", False)) or str(getattr(p, "status", "")).lower() in
                   {"active", "ativo", "enabled", "on", "1", "true"}
            ]
        return ListActivePlansOutput(plans=[_map_item(p) for p in plans])
