# infrastructure/persistence/sqlalchemy/models/transaction_model.py
from __future__ import annotations
from uuid import uuid4
from sqlalchemy import String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
from brasiltransporta.domain.entities.transaction import Transaction, TransactionStatus, PaymentMethod
from brasiltransporta.domain.value_objects.money import Money

class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="BRL")
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=TransactionStatus.PENDING.value)
    external_payment_id: Mapped[str] = mapped_column(String(100), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="transactions")
    plan = relationship("PlanModel")

    @classmethod
    def from_domain(cls, transaction: Transaction) -> "TransactionModel":
        return cls(
            id=transaction.id,
            user_id=transaction.user_id,
            plan_id=transaction.plan_id,
            amount=transaction.amount.amount,
            currency=transaction.amount.currency,
            payment_method=transaction.payment_method.value,
            status=transaction.status.value,
            external_payment_id=transaction.external_payment_id,
            metadata=transaction.metadata,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )

    def to_domain(self) -> Transaction:
        return Transaction(
            id=self.id,
            user_id=self.user_id,
            plan_id=self.plan_id,
            amount=Money(amount=self.amount, currency=self.currency),
            payment_method=PaymentMethod(self.payment_method),
            status=TransactionStatus(self.status),
            external_payment_id=self.external_payment_id,
            metadata=self.metadata,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
