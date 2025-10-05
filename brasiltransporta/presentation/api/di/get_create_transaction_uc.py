from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.transaction_repository import (
    SQLAlchemyTransactionRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.plan_repository import (
    SQLAlchemyPlanRepository,
)
from brasiltransporta.application.transactions.use_cases.create_transaction import CreateTransactionUseCase

def get_create_transaction_uc(
    db: Session = Depends(get_session)
) -> CreateTransactionUseCase:
    transaction_repo = SQLAlchemyTransactionRepository(db)
    user_repo = SQLAlchemyUserRepository(db)
    plan_repo = SQLAlchemyPlanRepository(db)
    return CreateTransactionUseCase(transaction_repo, user_repo, plan_repo)