from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.transaction_repository import (
    SQLAlchemyTransactionRepository,
)
from brasiltransporta.application.billing.use_cases.create_transaction import CreateTransactionUseCase

def get_create_transaction_uc(db: Session = Depends(get_session)) -> CreateTransactionUseCase:
    repo = SQLAlchemyTransactionRepository(db)
    return CreateTransactionUseCase(repo)
