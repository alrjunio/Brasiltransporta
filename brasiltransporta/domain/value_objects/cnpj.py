from dataclasses import dataclass
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class CNPJ:
    value: str

    def __post_init__(self):
        digits = "".join(filter(str.isdigit, self.value))
        if len(digits) != 14:
            raise ValidationError("CNPJ deve ter 14 dígitos.")
        object.__setattr__(self, "value", digits)

    def __str__(self) -> str:
        return self.value