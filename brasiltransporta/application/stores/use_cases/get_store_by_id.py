from uuid import UUID
from dataclasses import dataclass
from brasiltransporta.domain.repositories.store_repository import StoreRepository
from brasiltransporta.domain.errors import ValidationError

@dataclass
class GetStoreByIdUseCase:
    store_repo: StoreRepository
    session: any

    def execute(self, store_id: UUID):
        store = self.store_repo.get_by_id(store_id)
        if not store:
            raise ValidationError("Loja não encontrada.")
        return store
