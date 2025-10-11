from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from brasiltransporta.domain.entities.address import Address
from brasiltransporta.domain.entities.enums import StoreCategory

from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.enums import StoreCategory
from brasiltransporta.domain.repositories.store_repository import StoreRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.store import StoreModel


class SQLAlchemyStoreRepository(StoreRepository):
    def __init__(self, session: Session):
        self._s = session

    async def create(self, store: Store) -> Store:
        """Implementa o método create da interface"""
        obj = StoreModel(
            id=store.id,
            name=store.name,
            cnpj=getattr(store.cnpj, "value", None),
            owner_id=store.owner_id,
            # created_at=store.created_at,
        )
        self._s.add(obj)
        self._s.flush()
        self._s.commit()
        return store

    async def get_by_id(self, store_id: str) -> Optional[Store]:
        """Busca store por ID"""
        row = self._s.query(StoreModel).filter(StoreModel.id == store_id).first()
        
        if not row:
            return None
            
        # Criar Address placeholder (usar dados do banco quando disponíveis)
        address = Address.create(
            street="Rua Principal",
            city="São Paulo", 
            state="SP",
            zip_code="01234-567"
        )
    
        return Store(
            id=row.id,
            name=row.name,
            owner_id=row.owner_id,
            description="Loja de veículos",  # ✅ Valor padrão
            address=address,
            categories=[StoreCategory.PARTS_STORE],
            contact_phone="(00) 00000-0000",  # ✅ Valor padrão
            cnpj=getattr(row, 'cnpj', None)
        )

    async def get_by_owner_id(self, owner_id: str) -> List[Store]:
        """Busca stores por owner_id"""
        rows = self._s.query(StoreModel).filter(StoreModel.owner_id == UUID(owner_id)).all()
        return [
            Store(
                id=row.id,
                name=row.name,
                owner_id=row.owner_id,
                cnpj=row.cnpj,
                phone=None,
                location=None,
            )
            for row in rows
        ]

    async def update(self, store: Store) -> Store:
        """Atualiza um store existente"""
        obj = self._s.query(StoreModel).filter(StoreModel.id == store.id).first()
        if obj:
            obj.name = store.name
            obj.cnpj = getattr(store.cnpj, "value", None)
            # Atualizar outros campos conforme necessário
            self._s.commit()
        return store

    async def delete(self, store_id: str) -> bool:
        """Remove um store"""
        obj = self._s.query(StoreModel).filter(StoreModel.id == UUID(store_id)).first()
        if obj:
            self._s.delete(obj)
            self._s.commit()
            return True
        return False

    async def list_by_owner(self, owner_id: str) -> List[Store]:
        """Lista stores por owner - similar ao get_by_owner_id"""
        return await self.get_by_owner_id(owner_id)

    async def list_all(self, limit: int = 100) -> List[Store]:
        """Lista todos os stores com limite"""
        rows = self._s.query(StoreModel).limit(limit).all()
        return [
            Store(
                id=row.id,
                name=row.name,
                owner_id=row.owner_id,
                cnpj=row.cnpj,
                phone=None,
                location=None,
            )
            for row in rows
        ]

    async def list_by_category(self, category: StoreCategory) -> List[Store]:
        """Lista stores por categoria - placeholder"""
        # Implementar quando tiver campo de categoria no modelo
        return []

    async def list_active_stores(self) -> List[Store]:
        """Lista stores ativos - placeholder"""
        # Implementar quando tiver campo de status
        return await self.list_all()

    async def search_stores(self, query: str, category: Optional[StoreCategory] = None) -> List[Store]:
        """Busca stores por texto - placeholder"""
        # Implementar busca por nome/descrição
        rows = self._s.query(StoreModel).filter(StoreModel.name.ilike(f"%{query}%")).all()
        return [
            Store(
                id=row.id,
                name=row.name,
                owner_id=row.owner_id,
                cnpj=row.cnpj,
                phone=None,
                location=None,
            )
            for row in rows
        ]

    async def activate_store(self, store_id: str) -> bool:
        """Ativa um store - placeholder"""
        # Implementar quando tiver campo de status
        return True

    async def deactivate_store(self, store_id: str) -> bool:
        """Desativa um store - placeholder"""
        # Implementar quando tiver campo de status
        return True

    # Método add existente (mantido para compatibilidade)
    def add(self, store: Store) -> None:
        obj = StoreModel(
            id=store.id,
            name=store.name,
            owner_id=store.owner_id,
            description=store.description,
            contact_phone=store.contact_phone,
            cnpj=store.cnpj  
        )
        self._s.add(obj)
        self._s.flush() 
        self._s.commit()