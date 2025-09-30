# application/transactions/use_cases/get_transaction_by_id.py
from dataclasses import dataclass
from typing import Optional
from brasiltransporta.domain.repositories.transaction_repository import TransactionRepository

@dataclass(frozen=True)
class GetTransactionByIdOutput:
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    external_payment_id: Optional[str]
    metadata: dict
    created_at: str
    updated_at: str

class GetTransactionByIdUseCase:
    def __init__(self, transactions: TransactionRepository):
        self._transactions = transactions

    def execute(self, transaction_id: str) -> Optional[GetTransactionByIdOutput]:
        transaction = self._transactions.get_by_id(transaction_id)
        if not transaction:
            return None
        
        return GetTransactionByIdOutput(
            id=transaction.id,
            user_id=transaction.user_id,
            plan_id=transaction.plan_id,
            amount=transaction.amount.amount,
            currency=transaction.amount.currency,
            payment_method=transaction.payment_method.value,
            status=transaction.status.value,
            external_payment_id=transaction.external_payment_id,
            metadata=transaction.metadata,
            created_at=transaction.created_at.isoformat(),
            updated_at=transaction.updated_at.isoformat()
        )
