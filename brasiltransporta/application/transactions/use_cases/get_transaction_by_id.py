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

from dataclasses import dataclass
from typing import Optional, Any

@dataclass(frozen=True)
class GetTransactionByIdInput:
    transaction_id: str

@dataclass(frozen=True)
class GetTransactionByIdOutput:
    # Você pode deixar genérico; o controller normaliza o objeto retornado.
    value: Optional[Any] = None

class GetTransactionByIdUseCase:
    def __init__(self, repository=None):
        """
        repository: opcional; se fornecido, deve ter um método get_by_id(id: str) -> entidade/DTO
        """
        self._repo = repository

    def execute(self, input_data: GetTransactionByIdInput) -> Optional[Any]:
        """
        Retorna a entidade/DTO se houver repositório; caso contrário, None.
        Isso é suficiente para não quebrar os imports do controller/routers.
        """
        if self._repo is None:
            return None
        return self._repo.get_by_id(input_data.transaction_id)
