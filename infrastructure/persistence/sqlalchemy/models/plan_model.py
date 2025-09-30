# infrastructure/persistence/sqlalchemy/models/plan_model.py
from __future__ import annotations
from uuid import uuid4
from sqlalchemy import String, Text, Boolean, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.domain.value_objects.money import Money

class PlanModel(Base):
    __tablename__ = "plans"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    plan_type: Mapped[str] = mapped_column(String(20), nullable=False)
    billing_cycle: Mapped[str] = mapped_column(String(20), nullable=False)
    price_amount: Mapped[float] = mapped_column(nullable=False)
    price_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="BRL")
    max_ads: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    max_featured_ads: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    features: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    @classmethod
    def from_domain(cls, plan: Plan) -> "PlanModel":
        return cls(
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
            created_at=plan.created_at,
            updated_at=plan.updated_at
        )

    def to_domain(self) -> Plan:
        return Plan(
            id=self.id,
            name=self.name,
            description=self.description,
            plan_type=PlanType(self.plan_type),
            billing_cycle=BillingCycle(self.billing_cycle),
            price=Money(amount=self.price_amount, currency=self.price_currency),
            max_ads=self.max_ads,
            max_featured_ads=self.max_featured_ads,
            is_active=self.is_active,
            features=self.features,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
