from dataclasses import dataclass
from typing import Optional

from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.value_objects.location import Location
from brasiltransporta.domain.value_objects.phone_number import PhoneNumber
from brasiltransporta.domain.repositories.store_repository import StoreRepository
from brasiltransporta.domain.errors import ValidationError


@dataclass(frozen=True)
class CreateStoreInput:
    name: str
    cnpj: str
    owner_id: str
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass(frozen=True)
class CreateStoreOutput:
    store_id: str


class CreateStoreUseCase:
    def __init__(self, stores: StoreRepository):
        self._stores = stores

    def execute(self, data: CreateStoreInput) -> CreateStoreOutput:
        # 1) montar VO(s) opcionais
        phone_vo = PhoneNumber(data.phone) if data.phone else None

        if (data.latitude is None) ^ (data.longitude is None):
            # XOR: só um foi informado → inválido (evita localização “meio definida”)
            raise ValidationError("Para localização, informe latitude e longitude juntas ou nenhuma.")

        location_vo = (
            Location(latitude=data.latitude, longitude=data.longitude)
            if data.latitude is not None and data.longitude is not None
            else None
        )

        # 2) criar entidade de domínio (valida nome/cnpj no domínio)
        store = Store.create(
            name=data.name,
            cnpj=data.cnpj,
            owner_id=data.owner_id,
            phone=str(phone_vo) if phone_vo else None,
            location=location_vo,
        )

        # 3) persistir via contrato
        self._stores.add(store)

        # 4) retorno
        return CreateStoreOutput(store_id=store.id)
