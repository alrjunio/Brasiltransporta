from dataclasses import dataclass
from uuid import uuid4
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.price import Price

@dataclass
class Transaction:
    id: str
    user_id: str
    plan_id: str
    amount: Price
    status: str   # ex.: "pending", "paid", "failed"

    @classmethod
    def create(cls, user_id: str, plan_id: str, amount: float, status: str) -> "Transaction":
        if not user_id or not plan_id:
            raise ValidationError("Usuário e Plano são obrigatórios.")
        if amount <= 0:
            raise ValidationError("Valor da transação deve ser positivo.")
        if status not in ["pending", "paid", "failed"]:
            raise ValidationError("Status inválido para transação.")
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            plan_id=plan_id,
            amount=Price(amount),
            status=status
        )