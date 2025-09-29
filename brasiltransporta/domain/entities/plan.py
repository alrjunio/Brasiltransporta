from dataclasses import dataclass
from uuid import uuid4
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.price import Price

@dataclass
class Plan:
    id: str
    name: str
    price: Price
    max_ads: int

    @classmethod
    def create(cls, name: str, price: float, max_ads: int) -> "Plan":
        if not name or len(name.strip()) < 2:
            raise ValidationError("Nome do plano inválido.")
        if max_ads <= 0:
            raise ValidationError("Quantidade máxima de anúncios deve ser positiva.")
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            price=Price(price),
            max_ads=max_ads
        )