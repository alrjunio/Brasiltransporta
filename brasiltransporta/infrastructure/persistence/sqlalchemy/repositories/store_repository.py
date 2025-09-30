from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.repositories.store_repository import StoreRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.store import StoreModel


class SQLAlchemyStoreRepository(StoreRepository):
    def __init__(self, session: Session):
        self._s = session

    def add(self, store: Store) -> None:
        obj = StoreModel(
            id=store.id,
            name=store.name,
            cnpj=getattr(store.cnpj, "value", None),
            owner_id=store.owner_id,
            #created_at=store.created_at,
        )
        self._s.add(obj)
        self._s.flush() 
        self._s.commit() 


    def get_by_id(self, store_id: UUID) -> Optional[Store]:
        row = self._s.query(StoreModel).filter(StoreModel.id == store_id).first()
        if not row:
            return None
        return Store(
            id=row.id,
            name=row.name,
            owner_id=row.owner_id,  
            cnpj=row.cnpj,
            phone=None,  # ✅ Adicione estes campos
            location=None,  # ✅ Adicione estes campos
            #created_at=row.created_at,
        )