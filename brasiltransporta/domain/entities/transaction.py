from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

from brasiltransporta.domain.errors import ValidationError
from enum import Enum


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    FAILED = "failed"


class PaymentMethod(str, Enum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    BOLETO = "boleto"


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "BRL"


@dataclass
class Transaction:
    id: str
    user_id: str
    plan_id: str
    amount: Money
    currency: str
    payment_method: PaymentMethod
    status: TransactionStatus
    external_payment_id: Optional[str]
    metadata: Optional[dict]
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
            raise ValidationError("Valor da transação deve ser maior que zero")

        now = datetime.utcnow()
        return cls(
            id=str(uuid.uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=Money(amount, currency),
            currency=currency,
            payment_method=payment_method,
            status=TransactionStatus.PENDING,
            external_payment_id=None,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )

    # métodos “clássicos”
    def complete(self) -> None:
        self.status = TransactionStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def fail(self) -> None:
        self.status = TransactionStatus.FAILED
        self.updated_at = datetime.utcnow()

    def refund(self) -> None:
        if self.status != TransactionStatus.COMPLETED:
            raise ValidationError("Apenas transações completadas podem ser reembolsadas")
        self.status = TransactionStatus.REFUNDED
        self.updated_at = datetime.utcnow()

    # aliases esperados pelos testes
    def mark_completed(self, external_payment_id: str | None = None) -> None:
        self.external_payment_id = external_payment_id
        self.complete()

    def mark_failed(self) -> None:
        self.fail()


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
        # validações e mensagens iguais às dos testes
        if amount <= 0:
            raise ValidationError("Valor da transação deve ser maior que zero")

        now = datetime.utcnow()
        return cls(
            id=str(uuid.uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=Money(amount, currency),  # VO
            currency=currency,
            payment_method=payment_method,
            status=TransactionStatus.PENDING,
            external_payment_id=None,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )

    def complete(self) -> None:
        self.status = TransactionStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def fail(self) -> None:
        self.status = TransactionStatus.FAILED
        self.updated_at = datetime.utcnow()

    def refund(self) -> None:
        if self.status != TransactionStatus.COMPLETED:
            # usar ValidationError e a mensagem exata
            raise ValidationError("Apenas transações completadas podem ser reembolsadas")
        self.status = TransactionStatus.REFUNDED
        self.updated_at = datetime.utcnow()
