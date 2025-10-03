from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.application.plans.use_cases.create_plan import CreatePlanUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.plan_repository import (
    SQLAlchemyPlanRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session


def get_create_plan_uc(db: Session = Depends(get_session)) -> CreatePlanUseCase:
    repo = SQLAlchemyPlanRepository(db)
    return CreatePlanUseCase(repo)
