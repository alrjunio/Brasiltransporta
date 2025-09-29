from dataclasses import dataclass
from brasiltransporta.domain.entities.transaction import Transaction
from brasiltransporta.domain.value_objects.price import Price
from brasiltransporta.domain.repositories.transaction_repository import TransactionRepository
from brasiltransporta.domain.errors import ValidationError


@dataclass(frozen=True)
class CreateTransactionInput:
    user_id: str
    plan_id: str
    amount: float
    status: str = "pending"  # "pending" | "paid" | "failed"


@dataclass(frozen=True)
class CreateTransactionOutput:
    transaction_id: str


class CreateTransactionUseCase:
    def __init__(self, transactions: TransactionRepository):
        self._tx = transactions

    def execute(self, data: CreateTransactionInput) -> CreateTransactionOutput:
        # 1) validação adicional de aplicação (rápida)
        if not data.user_id or not data.plan_id:
            raise ValidationError("user_id e plan_id são obrigatórios.")
        if data.amount <= 0:
            raise ValidationError("amount deve ser positivo.")
        if data.status not in {"pending", "paid", "failed"}:
            raise ValidationError("status inválido. Use 'pending', 'paid' ou 'failed'.")

        # 2) construir VO/Entidade de domínio
        price = Price(data.amount)
        tx = Transaction.create(
            user_id=data.user_id,
            plan_id=data.plan_id,
            amount=price.amount,
            status=data.status,
        )

        # 3) persistir via contrato
        self._tx.add(tx)

        # 4) retorno
        return CreateTransactionOutput(transaction_id=tx.id)
