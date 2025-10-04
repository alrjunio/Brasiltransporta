from dataclasses import dataclass
from brasiltransporta.domain.errors.errors import ValidationError

@dataclass(frozen=True)
class Price:
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise ValidationError("Preço não pode ser negativo.")

    def __str__(self) -> str:
        return f"{self.amount:.2f}"
