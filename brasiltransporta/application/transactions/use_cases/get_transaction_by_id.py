from dataclasses import dataclass
from typing import Optional, Any

@dataclass(frozen=True)
class TransactionDetailOutput:
    id: str
    user_id: str
    plan_id: str
    amount: float          # <- os testes esperam float aqui
    currency: str
    payment_method: Any
    status: Any
    external_payment_id: Optional[str] = None
    metadata: dict | None = None
    created_at: Any = None
    updated_at: Any = None

class GetTransactionByIdUseCase:
    def __init__(self, transaction_repo) -> None:
        self._repo = transaction_repo

    def execute(self, transaction_id: str) -> Optional[TransactionDetailOutput]:
        tx = self._repo.get_by_id(transaction_id)
        if tx is None:
            return None

        # aceita VO Money ou float
        amount = getattr(tx.amount, "amount", tx.amount)
        return TransactionDetailOutput(
            id=str(tx.id),
            user_id=str(tx.user_id),
            plan_id=str(tx.plan_id),
            amount=float(amount),
            currency=str(getattr(tx, "currency", "BRL")),
            payment_method=getattr(tx, "payment_method", None),
            status=getattr(tx, "status", None),
            external_payment_id=getattr(tx, "external_payment_id", None),
            metadata=getattr(tx, "metadata", None),
            created_at=getattr(tx, "created_at", None),
            updated_at=getattr(tx, "updated_at", None),
        )
