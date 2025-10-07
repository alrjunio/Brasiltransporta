# domain/repositories/vehicle_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from brasiltransporta.domain.entities.vehicle import Vehicle
from brasiltransporta.domain.entities.enums import VehicleBrand, VehicleType, VehicleCondition

class VehicleRepository(ABC):
    
    @abstractmethod
    async def create(self, vehicle: Vehicle) -> Vehicle:
        pass
    
    @abstractmethod
    async def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        pass
    
    @abstractmethod
    async def update(self, vehicle: Vehicle) -> Vehicle:
        pass
    
    @abstractmethod
    async def delete(self, vehicle_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_by_owner(self, owner_id: str) -> List[Vehicle]:
        pass
    
    @abstractmethod
    async def list_all(self, limit: int = 100) -> List[Vehicle]:
        pass
    
    @abstractmethod
    async def list_by_store(self, store_id: str) -> List[Vehicle]:
        pass
    
    @abstractmethod
    async def filter_vehicles(
        self,
        brand: Optional[VehicleBrand] = None,
        vehicle_type: Optional[VehicleType] = None,
        condition: Optional[VehicleCondition] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        store_id: Optional[str] = None,
        implement_segment: Optional[str] = None
    ) -> List[Vehicle]:
        pass
    
    @abstractmethod
    async def search_vehicles(self, query: str) -> List[Vehicle]:
        pass
    
    @abstractmethod
    async def count_by_store(self, store_id: str) -> int:
        pass