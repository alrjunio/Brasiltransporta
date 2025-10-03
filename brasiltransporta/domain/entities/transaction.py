from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional
from enum import Enum

class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    PIX = "pix"
    BOLETO = "boleto"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class Transaction:
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str = "BRL"
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    status: TransactionStatus = TransactionStatus.PENDING
    external_payment_id: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, user_id: str, plan_id: str, amount: float, payment_method: PaymentMethod, currency: str = "BRL", metadata: Optional[dict]=None) -> "Transaction":
        if amount <= 0:
            # testes de domínio esperam ValueError (não ValidationError)
            raise ValueError("Valor da transação deve ser maior que zero")
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=float(amount),
            currency=currency,
            payment_method=payment_method,
            status=TransactionStatus.PENDING,
            metadata=metadata or None,
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
            # testes de domínio esperam ValueError e mensagem SEM ponto final
            raise ValueError("Apenas transações completadas podem ser reembolsadas")
        self.status = TransactionStatus.REFUNDED
        self.updated_at = datetime.utcnow()
