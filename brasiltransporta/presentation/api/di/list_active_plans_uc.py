from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.application.plans.use_cases.list_active_plans import ListActivePlansUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.plan_repository import (
    SQLAlchemyPlanRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session


def get_list_active_plans_uc(db: Session = Depends(get_session)) -> ListActivePlansUseCase:
    repo = SQLAlchemyPlanRepository(db)
    return ListActivePlansUseCase(repo)
