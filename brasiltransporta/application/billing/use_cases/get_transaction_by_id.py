# brasiltransporta/application/billing/use_cases/get_transaction_by_id.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from brasiltransporta.domain.repositories.transaction_repository import TransactionRepository
from brasiltransporta.domain.entities.transaction import Transaction  # entidade de domínio


@dataclass(frozen=True)
class TransactionDetailOutput:
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    external_payment_id: Optional[str]
    metadata: dict
    created_at: datetime
    updated_at: datetime


class GetTransactionByIdUseCase:
    """
    Retorna os dados de uma transação por ID no formato pronto para resposta.
    Se não encontrar, retorna None (a rota deve transformar em 404).
    """
    def __init__(self, transactions: TransactionRepository):
        self._tx = transactions

    def execute(self, transaction_id: str) -> Optional[TransactionDetailOutput]:
        if not transaction_id:
            return None

        tx: Optional[Transaction] = self._tx.get_by_id(transaction_id)
        if tx is None:
            return None

        # Transforma enums em string para serializar corretamente
        payment_method = getattr(tx.payment_method, "value", str(tx.payment_method))
        status = getattr(tx.status, "value", str(tx.status))

        return TransactionDetailOutput(
            id=tx.id,
            user_id=tx.user_id,
            plan_id=tx.plan_id,
            amount=tx.amount,                    # sua entidade usa float (sem VO Price aqui)
            currency=getattr(tx, "currency", "BRL"),
            payment_method=payment_method,
            status=status,
            external_payment_id=tx.external_payment_id,
            metadata=getattr(tx, "metadata", {}) or {},
            created_at=tx.created_at,
            updated_at=tx.updated_at,
        )
