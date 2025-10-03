from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum

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
    price_amount: float
    price_currency: str
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
            raise ValueError("Nome do plano deve ter pelo menos 3 caracteres.")
        if price_amount < 0:
            raise ValueError("Preço não pode ser negativo.")
        if max_ads < 0:
            raise ValueError("Número máximo de anúncios não pode ser negativo.")

        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            description=description.strip(),
            plan_type=plan_type,
            billing_cycle=billing_cycle,
            price_amount=price_amount,
            price_currency=price_currency,
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
