from dataclasses import asdict
from typing import List

try:
    from brasiltransporta.domain.repositories.plan_repository import PlanRepository
except Exception:  # fallback: defina sua interface real
    class PlanRepository:  # type: ignore
        def list_active(self): ...
        def list_all(self): ...

from brasiltransporta.application.billing.use_cases.get_plan_by_id import (
    PlanDetailOutput,
    _to_status_and_active,
    _to_price_and_currency,
    _to_features,
)

def _map_plan(plan) -> PlanDetailOutput:
    status_str, is_active = _to_status_and_active(plan)
    amount, currency = _to_price_and_currency(plan)
    duration = getattr(plan, "duration_days", getattr(plan, "duration", None))
    return PlanDetailOutput(
        id=plan.id,
        name=plan.name,
        description=getattr(plan, "description", None),
        price=amount,
        currency=currency,
        duration_days=duration,
        features=_to_features(plan),
        status=status_str,
        is_active=is_active,
        created_at=plan.created_at,
        updated_at=getattr(plan, "updated_at", None),
    )

class ListActivePlansUseCase:
    """
    Retorna a lista de planos ativos.
    Tenta usar PlanRepository.list_active(); se não existir, filtra list_all().
    """
    def __init__(self, plans: PlanRepository):
        self._plans = plans

    def execute(self) -> List[PlanDetailOutput]:
        try:
            plans = self._plans.list_active()
        except Exception:
            all_plans = self._plans.list_all()
            plans = [
                p for p in all_plans
                if getattr(p, "is_active", None) is True
                or str(getattr(p, "status", "")).lower() in {"active", "ativo", "enabled", "on", "1", "true"}
            ]
        return [ _map_plan(p) for p in plans ]