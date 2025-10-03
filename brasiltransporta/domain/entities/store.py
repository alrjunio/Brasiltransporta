from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.cnpj import CNPJ
from brasiltransporta.domain.value_objects.phone_number import PhoneNumber
from brasiltransporta.domain.value_objects.location import Location

@dataclass
class Store:
    id: str
    name: str
    cnpj: CNPJ
    phone: Optional[PhoneNumber]
    location: Optional[Location]
    owner_id: str        # relacionamento: Usuário dono da loja

    @classmethod
    def create(
        cls,
        name: str,
        cnpj: str,
        owner_id: str,
        phone: Optional[str] = None,
        location: Optional[Location] = None,
    ) -> "Store":
        if not name or len(name.strip()) < 2:
            raise ValidationError("Nome da loja inválido.")
        cnpj_vo = CNPJ(cnpj)
        phone_vo = PhoneNumber(phone) if phone else None
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            cnpj=cnpj_vo,
            phone=phone_vo,
            location=location,
            owner_id=owner_id
        )