# domain/entities/plan.py
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.money import Money

class PlanType(Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class BillingCycle(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

@dataclass
class Plan:
    id: str
    name: str
    description: str
    plan_type: PlanType
    billing_cycle: BillingCycle
    price: Money
    max_ads: int
    max_featured_ads: int
    is_active: bool
    features: list[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        plan_type: PlanType,
        billing_cycle: BillingCycle,
        price_amount: float,
        price_currency: str = "BRL",
        max_ads: int = 10,
        max_featured_ads: int = 1,
        features: Optional[list[str]] = None
    ) -> "Plan":
        if not name or len(name.strip()) < 3:
            raise ValidationError("Nome do plano deve ter pelo menos 3 caracteres.")
        if price_amount < 0:
            raise ValidationError("Preço não pode ser negativo.")
        if max_ads < 0:
            raise ValidationError("Número máximo de anúncios não pode ser negativo.")

        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            description=description.strip(),
            plan_type=plan_type,
            billing_cycle=billing_cycle,
            price=Money(amount=price_amount, currency=price_currency),
            max_ads=max_ads,
            max_featured_ads=max_featured_ads,
            is_active=True,
            features=features or [],
            created_at=now,
            updated_at=now
        )

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.utcnow()
