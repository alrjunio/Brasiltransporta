# domain/repositories/advertisement_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.entities.enums import AdvertisementStatus

class AdvertisementRepository(ABC):
    
    @abstractmethod
    async def create(self, advertisement: Advertisement) -> Advertisement:
        pass
    
    @abstractmethod
    async def get_by_id(self, advertisement_id: str) -> Optional[Advertisement]:
        pass
    
    @abstractmethod
    async def update(self, advertisement: Advertisement) -> Advertisement:
        pass
    
    @abstractmethod
    async def delete(self, advertisement_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_by_store(self, store_id: str, limit: int = 50) -> List[Advertisement]:
        pass
    
    @abstractmethod
    async def list_by_vehicle(self, vehicle_id: str) -> List[Advertisement]:
        pass
    
    @abstractmethod
    async def list_by_status(self, status: AdvertisementStatus) -> List[Advertisement]:
        pass
    
    @abstractmethod
    async def list_active(self, region: Optional[str] = None, limit: int = 50) -> List[Advertisement]:
        pass
    
    @abstractmethod
    async def list_featured(self, limit: int = 20) -> List[Advertisement]:
        pass
    
    @abstractmethod
    async def update_images(self, advertisement_id: str, images: List[str]) -> bool:
        pass
    
    @abstractmethod
    async def update_videos(self, advertisement_id: str, videos: List[str]) -> bool:
        pass
    
    @abstractmethod
    async def search_ads(self, query: str, category: Optional[str] = None) -> List[Advertisement]:
        pass
    
    @abstractmethod
    async def increment_views(self, advertisement_id: str) -> bool:
        pass