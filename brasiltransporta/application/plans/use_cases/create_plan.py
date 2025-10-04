from dataclasses import dataclass
from typing import Optional, Any

from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.domain.repositories.plan_repository import PlanRepository
from brasiltransporta.domain.errors.errors import ValidationError


@dataclass(frozen=True)
class CreatePlanInput:
    name: str
    description: Optional[str]
    plan_type: PlanType | str
    billing_cycle: BillingCycle | str
    price_amount: float
    price_currency: str = "BRL"
    max_ads: int = 10
    max_featured_ads: int = 1
    features: list[str] | None = None

@dataclass(frozen=True)
class CreatePlanOutput:
    plan_id: str

def _to_enum(v: Any, enum_cls):
    if isinstance(v, enum_cls):
        return v
    return enum_cls(str(v))

class CreatePlanUseCase:
    def __init__(self, plans: PlanRepository) -> None:
        self._plans = plans

    def execute(self, inp: CreatePlanInput) -> CreatePlanOutput:
        plan_type = _to_enum(inp.plan_type, PlanType)
        billing_cycle = _to_enum(inp.billing_cycle, BillingCycle)

        # regra exigida pelos testes
        existing = self._plans.get_by_type_and_cycle(plan_type, billing_cycle)
        if existing is not None:
            raise ValidationError("Já existe um plano com este tipo e ciclo de cobrança")

        plan = Plan.create(
            name=inp.name,
            description=inp.description or "",
            plan_type=plan_type,
            billing_cycle=billing_cycle,
            price_amount=inp.price_amount,
            price_currency=inp.price_currency,
            max_ads=inp.max_ads,
            max_featured_ads=inp.max_featured_ads,
            features=inp.features or [],
        )
        self._plans.add(plan)
        return CreatePlanOutput(plan_id=str(plan.id))
