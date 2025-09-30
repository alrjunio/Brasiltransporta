# application/transactions/use_cases/create_transaction.py
from dataclasses import dataclass
from brasiltransporta.domain.repositories.transaction_repository import TransactionRepository
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.domain.repositories.plan_repository import PlanRepository
from brasiltransporta.domain.entities.transaction import Transaction, PaymentMethod
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class CreateTransactionInput:
    user_id: str
    plan_id: str
    amount: float
    payment_method: PaymentMethod
    currency: str = "BRL"
    metadata: dict = None

@dataclass(frozen=True)
class CreateTransactionOutput:
    transaction_id: str

class CreateTransactionUseCase:
    def __init__(
        self, 
        transactions: TransactionRepository,
        users: UserRepository,
        plans: PlanRepository
    ):
        self._transactions = transactions
        self._users = users
        self._plans = plans

    def execute(self, data: CreateTransactionInput) -> CreateTransactionOutput:
        # Validar se user existe
        user = self._users.get_by_id(data.user_id)
        if not user:
            raise ValidationError("Usuário não encontrado.")

        # Validar se plan existe e está ativo
        plan = self._plans.get_by_id(data.plan_id)
        if not plan or not plan.is_active:
            raise ValidationError("Plano não encontrado ou inativo.")

        # Validar se amount corresponde ao preço do plano
        if data.amount != plan.price.amount:
            raise ValidationError("Valor da transação não corresponde ao preço do plano.")

        transaction = Transaction.create(
            user_id=data.user_id,
            plan_id=data.plan_id,
            amount=data.amount,
            payment_method=data.payment_method,
            currency=data.currency,
            metadata=data.metadata
        )

        self._transactions.add(transaction)
        return CreateTransactionOutput(transaction_id=transaction.id)
