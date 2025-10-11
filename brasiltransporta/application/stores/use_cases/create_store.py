# Volte o create_store.py para a versão ORIGINAL que aceita cnpj
from dataclasses import dataclass
from typing import Optional

from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.value_objects.location import Location
from brasiltransporta.domain.value_objects.phone_number import PhoneNumber
from brasiltransporta.domain.repositories.store_repository import StoreRepository
from brasiltransporta.domain.errors.errors import ValidationError


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
        # Usar create_simple que é compatível
        store = Store.create_simple(
            name=data.name,
            owner_id=data.owner_id,
            cnpj=data.cnpj
        )
        
        self._stores.add(store)
        return CreateStoreOutput(store_id=store.id)