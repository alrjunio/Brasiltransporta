from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.application.transactions.use_cases.get_transaction_by_id import GetTransactionByIdUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.transaction_repository import (
    SQLAlchemyTransactionRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session

def get_get_transaction_by_id_uc(db: Session = Depends(get_session)) -> GetTransactionByIdUseCase:
    repo = SQLAlchemyTransactionRepository(db)
    return GetTransactionByIdUseCase(repo)