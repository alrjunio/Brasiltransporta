from dataclasses import dataclass
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        digits = "".join(filter(str.isdigit, self.value))
        if len(digits) < 10:
            raise ValidationError("Telefone inválido.")
        object.__setattr__(self, "value", digits)

    def __str__(self) -> str:
        return self.value