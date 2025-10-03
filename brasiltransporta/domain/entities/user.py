from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.email import Email
from brasiltransporta.domain.value_objects.phone_number import PhoneNumber

@dataclass
class User:
    id: str
    name: str
    email: Email
    password_hash: str
    phone: Optional[PhoneNumber] = None
    birth_date: Optional[str] = None   # ISO "YYYY-MM-DD"
    profession: Optional[str] = None
    region: Optional[str] = None       # ex.: "Sudeste"

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        password_hash: str,
        phone: Optional[str] = None,
        birth_date: Optional[str] = None,
        profession: Optional[str] = None,
        region: Optional[str] = None,
    ) -> "User":
        if not name or len(name.strip()) < 2:
            raise ValidationError("Nome inválido.")
        email_vo = Email(email)
        phone_vo = PhoneNumber(phone) if phone else None
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            email=email_vo,
            password_hash=password_hash,
            phone=phone_vo,
            birth_date=birth_date,
            profession=profession,
            region=region,
        )