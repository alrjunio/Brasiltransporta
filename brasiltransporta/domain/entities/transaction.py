from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from brasiltransporta.domain.value_objects.money import Money
from brasiltransporta.domain.errors.errors import ValidationError

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    PIX = "pix"  
    
@dataclass
class Transaction:
    id: str
    user_id: str
    plan_id: str
    amount: Money
    payment_method: PaymentMethod
    status: TransactionStatus = field(default=TransactionStatus.PENDING)
    currency: str = field(default="BRL")
    external_payment_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        user_id: str,
        plan_id: str,
        amount: float,
        payment_method: PaymentMethod,
        currency: str = "BRL",
        metadata: Optional[Dict[str, Any]] = None
    ) -> "Transaction":
        if amount is None or float(amount) <= 0:
            # TESTE espera ValidationError com essa mensagem
            raise ValidationError("Valor da transação deve ser maior que zero")

        return cls(
            id=str(uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=Money(float(amount), currency),
            payment_method=payment_method,
            currency=currency,
            metadata=metadata
        )

    def mark_completed(self, external_id: str) -> None:
        self.status = TransactionStatus.COMPLETED
        self.external_payment_id = external_id
        self.updated_at = datetime.utcnow()

    def mark_failed(self) -> None:
        self.status = TransactionStatus.FAILED
        self.updated_at = datetime.utcnow()

    def refund(self) -> None:
        # TESTE espera ValidationError e mensagem SEM ponto final
        if self.status != TransactionStatus.COMPLETED:
            raise ValidationError("Apenas transações completadas podem ser reembolsadas")
        self.status = TransactionStatus.REFUNDED
        self.updated_at = datetime.utcnow()
