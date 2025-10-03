from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.domain.repositories.plan_repository import PlanRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.plan import PlanModel  # <- caminho real


class SQLAlchemyPlanRepository(PlanRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, plan: Plan) -> None:
        model = PlanModel.from_domain(plan)
        self._session.add(model)
        self._session.flush()
        self._session.commit()

    def get_by_id(self, plan_id: str) -> Optional[Plan]:
        stmt = select(PlanModel).where(PlanModel.id == plan_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def get_by_type_and_cycle(self, plan_type: PlanType, billing_cycle: BillingCycle) -> Optional[Plan]:
        stmt = select(PlanModel).where(
            PlanModel.plan_type == plan_type.value,
            PlanModel.billing_cycle == billing_cycle.value,
            PlanModel.is_active == True,
        )
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def list_active(self) -> List[Plan]:
        stmt = select(PlanModel).where(PlanModel.is_active == True).order_by(PlanModel.created_at.desc())
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def update(self, plan: Plan) -> None:
        stmt = select(PlanModel).where(PlanModel.id == plan.id)
        model = self._session.execute(stmt).scalar_one_or_none()
        if not model:
            return
        model.name = plan.name
        model.description = plan.description
        model.plan_type = plan.plan_type.value if hasattr(plan.plan_type, "value") else str(plan.plan_type)
        model.billing_cycle = plan.billing_cycle.value if hasattr(plan.billing_cycle, "value") else str(plan.billing_cycle)
        # campos de preço corretos (sem VO Price)
        model.price_amount = plan.price_amount
        model.price_currency = plan.price_currency
        model.max_ads = plan.max_ads
        model.max_featured_ads = plan.max_featured_ads
        model.is_active = plan.is_active
        model.features = plan.features
        model.updated_at = plan.updated_at
        self._session.flush()
        self._session.commit()
