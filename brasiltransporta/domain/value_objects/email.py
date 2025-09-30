# brasiltransporta/domain/value_objects/email.py
import re
from dataclasses import dataclass

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self):
        v = (self.value or "").strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("Invalid email address")
        # como a dataclass é frozen, use object.__setattr__ para ajustar o valor normalizado
        object.__setattr__(self, "value", v)

    def __str__(self) -> str:
        return self.value

    

 