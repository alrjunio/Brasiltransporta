import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, Text, Boolean, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID

from .base import Base  # ajuste se seu Base estiver em outro módulo

from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle


class PlanModel(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    plan_type = Column(String(20), nullable=False)
    billing_cycle = Column(String(20), nullable=False)
    price_amount = Column(Numeric(12, 2), nullable=False)
    price_currency = Column(String(3), nullable=False, default="BRL")
    max_ads = Column(Integer, nullable=False, default=10)
    max_featured_ads = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)
    features = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @classmethod
    def from_domain(cls, p: Plan) -> "PlanModel":
        return cls(
            id=uuid.UUID(p.id) if isinstance(p.id, str) else p.id,
            name=p.name,
            description=p.description,
            plan_type=p.plan_type.value if hasattr(p.plan_type, "value") else str(p.plan_type),
            billing_cycle=p.billing_cycle.value if hasattr(p.billing_cycle, "value") else str(p.billing_cycle),
            price_amount=p.price_amount,
            price_currency=p.price_currency,
            max_ads=p.max_ads,
            max_featured_ads=p.max_featured_ads,
            is_active=p.is_active,
            features=p.features or [],
            created_at=p.created_at,
            updated_at=p.updated_at,
        )

    def to_domain(self) -> Plan:
        pt = self.plan_type
        bc = self.billing_cycle
        try:
            pt = PlanType(pt)
        except Exception:
            pass
        try:
            bc = BillingCycle(bc)
        except Exception:
            pass

        return Plan(
            id=str(self.id),
            name=self.name,
            description=self.description,
            plan_type=pt,
            billing_cycle=bc,
            price_amount=float(self.price_amount),
            price_currency=self.price_currency,
            max_ads=self.max_ads,
            max_featured_ads=self.max_featured_ads,
            is_active=self.is_active,
            features=self.features or [],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
