# application/plans/use_cases/create_plan.py
from dataclasses import dataclass
from brasiltransporta.domain.repositories.plan_repository import PlanRepository
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class CreatePlanInput:
    name: str
    description: str
    plan_type: PlanType
    billing_cycle: BillingCycle
    price_amount: float
    price_currency: str = "BRL"
    max_ads: int = 10
    max_featured_ads: int = 1
    features: list[str] = None

@dataclass(frozen=True)
class CreatePlanOutput:
    plan_id: str

class CreatePlanUseCase:
    def __init__(self, plans: PlanRepository):
        self._plans = plans

    def execute(self, data: CreatePlanInput) -> CreatePlanOutput:
        # Verificar se já existe plano com mesmo tipo e ciclo
        existing = self._plans.get_by_type_and_cycle(data.plan_type, data.billing_cycle)
        if existing:
            raise ValidationError("Já existe um plano com este tipo e ciclo de cobrança.")

        plan = Plan.create(
            name=data.name,
            description=data.description,
            plan_type=data.plan_type,
            billing_cycle=data.billing_cycle,
            price_amount=data.price_amount,
            price_currency=data.price_currency,
            max_ads=data.max_ads,
            max_featured_ads=data.max_featured_ads,
            features=data.features or []
        )

        self._plans.add(plan)
        return CreatePlanOutput(plan_id=plan.id)
