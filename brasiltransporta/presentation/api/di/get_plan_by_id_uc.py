from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.application.plans.use_cases.get_plan_by_id import GetPlanByIdUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.plan_repository import (
    SQLAlchemyPlanRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session


def get_plan_by_id_uc(db: Session = Depends(get_session)) -> GetPlanByIdUseCase:
    repo = SQLAlchemyPlanRepository(db)
    return GetPlanByIdUseCase(repo)
