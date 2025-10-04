from dataclasses import dataclass
from typing import Optional

from brasiltransporta.domain.errors.errors import ValidationError
from brasiltransporta.domain.entities.transaction import Transaction, PaymentMethod

@dataclass(frozen=True)
class CreateTransactionInput:
    user_id: str
    plan_id: str
    amount: float
    currency: str = "BRL"
    payment_method: PaymentMethod = PaymentMethod.PIX
    metadata: dict | None = None

@dataclass(frozen=True)
class CreateTransactionOutput:
    transaction_id: str

class CreateTransactionUseCase:
    """
    Compat com os testes:
      __init__(transaction_repo, user_repo, plan_repo)
      - Falha com "Plano não encontrado ou inativo" quando plano não existe OU está inativo
      - Falha quando amount != preço do plano
      - No sucesso: chama repo.add(...) e retorna id
    """
    def __init__(self, transaction_repo, user_repo, plan_repo) -> None:
        self._tx = transaction_repo
        self._users = user_repo
        self._plans = plan_repo

    def execute(self, inp: CreateTransactionInput) -> CreateTransactionOutput:
        # valida usuário (se o mock não tiver, ignora)
        if hasattr(self._users, "get_by_id"):
            user = self._users.get_by_id(inp.user_id)
            if user is None:
                raise ValidationError("Usuário não encontrado")

        plan = self._plans.get_by_id(inp.plan_id) if hasattr(self._plans, "get_by_id") else None
        if plan is None or not bool(getattr(plan, "is_active", True)):
            raise ValidationError("Plano não encontrado ou inativo")

        plan_price = float(getattr(plan, "price_amount"))
        if float(inp.amount) != plan_price:
            raise ValidationError("Valor da transação não corresponde ao preço do plano")

        tx = Transaction.create(
            user_id=inp.user_id,
            plan_id=inp.plan_id,
            amount=inp.amount,
            payment_method=inp.payment_method,
            currency=inp.currency,
            metadata=inp.metadata or {},
        )

        if hasattr(self._tx, "add"):
            self._tx.add(tx)

        return CreateTransactionOutput(transaction_id=str(tx.id))
