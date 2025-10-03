# infrastructure/persistence/sqlalchemy/repositories/transaction_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from brasiltransporta.domain.entities.transaction import Transaction, TransactionStatus
from brasiltransporta.domain.repositories.transaction_repository import TransactionRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.transaction import TransactionModel

class SQLAlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, transaction: Transaction) -> None:
        model = TransactionModel.from_domain(transaction)
        self._session.add(model)

    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        stmt = select(TransactionModel).where(TransactionModel.id == transaction_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def get_by_external_id(self, external_id: str) -> Optional[Transaction]:
        stmt = select(TransactionModel).where(TransactionModel.external_payment_id == external_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def list_by_user(self, user_id: str, limit: int = 50) -> List[Transaction]:
        stmt = select(TransactionModel).where(
            TransactionModel.user_id == user_id
        ).order_by(TransactionModel.created_at.desc()).limit(limit)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def list_by_status(self, status: TransactionStatus, limit: int = 50) -> List[Transaction]:
        stmt = select(TransactionModel).where(
            TransactionModel.status == status.value
        ).order_by(TransactionModel.created_at.desc()).limit(limit)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def update(self, transaction: Transaction) -> None:
        stmt = select(TransactionModel).where(TransactionModel.id == transaction.id)
        model = self._session.execute(stmt).scalar_one_or_none()
        if model:
            model.amount = transaction.amount.amount
            model.currency = transaction.amount.currency
            model.payment_method = transaction.payment_method.value
            model.status = transaction.status.value
            model.external_payment_id = transaction.external_payment_id
            model.metadata = transaction.metadata
            model.updated_at = transaction.updated_at
