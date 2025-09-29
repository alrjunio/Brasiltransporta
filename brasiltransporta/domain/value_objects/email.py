# brasiltransporta/domain/value_objects/email.py
import re
from dataclasses import dataclass
from brasiltransporta.domain.errors import ValidationError

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        # valida formato básico (usuario@dominio.tld)
        if not self.value or not _EMAIL_RE.match(self.value):
            raise ValidationError("Email inválido.")

    def __str__(self) -> str:
        # padroniza para minúsculo (evita duplicidade por casing)
        return self.value.lower()
