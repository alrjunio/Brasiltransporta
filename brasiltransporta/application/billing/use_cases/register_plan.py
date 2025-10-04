from dataclasses import dataclass
from brasiltransporta.domain.entities.plan import Plan
from brasiltransporta.domain.value_objects.price import Price
from brasiltransporta.domain.repositories.plan_repository import PlanRepository
from brasiltransporta.domain.errors.errors import ValidationError


@dataclass(frozen=True)
class RegisterPlanInput:
    name: str
    price: float
    max_ads: int


@dataclass(frozen=True)
class RegisterPlanOutput:
    plan_id: str


class RegisterPlanUseCase:
    def __init__(self, plans: PlanRepository):
        self._plans = plans

    def execute(self, data: RegisterPlanInput) -> RegisterPlanOutput:
        # 1) validações adicionais de aplicação (se precisar)
        if data.price <= 0:
            raise ValidationError("Preço do plano deve ser positivo.")
        if data.max_ads <= 0:
            raise ValidationError("Limite de anúncios deve ser maior que zero.")

        # 2) construir VOs/Entidade de domínio
        price_vo = Price(data.price)
        plan = Plan.create(name=data.name, price=price_vo.amount, max_ads=data.max_ads)

        # 3) persistir via contrato
        self._plans.add(plan)

        # 4) retorno
        return RegisterPlanOutput(plan_id=plan.id)
