# domain/entities/transaction.py
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.money import Money

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PIX = "pix"
    BOLETO = "boleto"
    BANK_TRANSFER = "bank_transfer"

@dataclass
class Transaction:
    id: str
    user_id: str
    plan_id: str
    amount: Money
    payment_method: PaymentMethod
    status: TransactionStatus
    external_payment_id: Optional[str]
    metadata: dict
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: str,
        plan_id: str,
        amount: float,
        payment_method: PaymentMethod,
        currency: str = "BRL",
        metadata: Optional[dict] = None
    ) -> "Transaction":
        if amount <= 0:
            raise ValidationError("Valor da transação deve ser maior que zero.")

        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=Money(amount=amount, currency=currency),
            payment_method=payment_method,
            status=TransactionStatus.PENDING,
            external_payment_id=None,
            metadata=metadata or {},
            created_at=now,
            updated_at=now
        )

    def mark_completed(self, external_payment_id: str) -> None:
        self.status = TransactionStatus.COMPLETED
        self.external_payment_id = external_payment_id
        self.updated_at = datetime.utcnow()

    def mark_failed(self) -> None:
        self.status = TransactionStatus.FAILED
        self.updated_at = datetime.utcnow()

    def refund(self) -> None:
        if self.status != TransactionStatus.COMPLETED:
            raise ValidationError("Apenas transações completadas podem ser reembolsadas.")
        self.status = TransactionStatus.REFUNDED
        self.updated_at = datetime.utcnow()
