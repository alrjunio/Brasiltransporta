# domain/repositories/store_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.enums import StoreCategory

class StoreRepository(ABC):
    
    @abstractmethod
    async def create(self, store: Store) -> Store:
        pass
    
    @abstractmethod
    async def get_by_id(self, store_id: str) -> Optional[Store]:
        pass
    
    @abstractmethod
    async def get_by_owner_id(self, owner_id: str) -> List[Store]:
        pass
    
    @abstractmethod
    async def update(self, store: Store) -> Store:
        pass
    
    @abstractmethod
    async def delete(self, store_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_by_owner(self, owner_id: str) -> List[Store]:
        pass
    
    @abstractmethod
    async def list_all(self, limit: int = 100) -> List[Store]:
        pass
    
    @abstractmethod
    async def list_by_category(self, category: StoreCategory) -> List[Store]:
        pass
    
    @abstractmethod
    async def list_active_stores(self) -> List[Store]:
        pass
    
    @abstractmethod
    async def search_stores(self, query: str, category: Optional[StoreCategory] = None) -> List[Store]:
        pass
    
    @abstractmethod
    async def activate_store(self, store_id: str) -> bool:
        pass
    
    @abstractmethod
    async def deactivate_store(self, store_id: str) -> bool:
        pass