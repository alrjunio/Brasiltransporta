# infrastructure/persistence/sqlalchemy/repositories/vehicle_repository.py
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from brasiltransporta.domain.entities.vehicle import Vehicle
from brasiltransporta.domain.entities.enums import VehicleBrand, VehicleType, VehicleCondition
from brasiltransporta.domain.repositories.vehicle_repository import VehicleRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.vehicle import VehicleModel

class SQLAlchemyVehicleRepository(VehicleRepository):  # ← AGORA IMPLEMENTA A INTERFACE
    def __init__(self, session: Session) -> None:
        self._session = session

    # --- MÉTODOS PRINCIPAIS ---
    async def create(self, vehicle: Vehicle) -> Vehicle:
        """Cria um novo veículo (substitui add)"""
        model = VehicleModel.from_domain(vehicle)
        self._session.add(model)
        self._session.commit()
        return model.to_domain()

    async def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        try:
            vehicle_uuid = UUID(vehicle_id)
        except ValueError:
            return None
            
        model = self._session.get(VehicleModel, vehicle_uuid)
        return model.to_domain() if model else None

    async def update(self, vehicle: Vehicle) -> Vehicle:
        """Atualiza todos os campos do veículo"""
        try:
            vehicle_uuid = UUID(vehicle.id)
        except ValueError:
            raise ValueError("Invalid vehicle ID")
            
        model = self._session.get(VehicleModel, vehicle_uuid)
        if not model:
            raise ValueError(f"Vehicle {vehicle.id} not found")
        
        # Atualiza todos os campos
        model.brand = vehicle.brand.value  # ← Converte Enum para string
        model.model = vehicle.model
        model.year = vehicle.year
        model.plate = vehicle.plate
        model.vehicle_type = vehicle.vehicle_type.value  # ← NOVO
        model.condition = vehicle.condition.value  # ← NOVO
        model.price = float(vehicle.price)  # ← NOVO (Decimal para float)
        model.implement_segment = vehicle.implement_segment.value if vehicle.implement_segment else None  # ← NOVO
        model.description = vehicle.description  # ← NOVO
        model.mileage = vehicle.mileage  # ← NOVO
        model.color = vehicle.color  # ← NOVO
        model.engine_power = vehicle.engine_power  # ← NOVO
        model.axle_configuration = vehicle.axle_configuration  # ← NOVO
        model.updated_at = vehicle.updated_at
        
        self._session.commit()
        return model.to_domain()

    async def delete(self, vehicle_id: str) -> bool:
        try:
            vehicle_uuid = UUID(vehicle_id)
        except ValueError:
            return False
            
        model = self._session.get(VehicleModel, vehicle_uuid)
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False

    # --- MÉTODOS DE CONSULTA ---
    async def list_by_owner(self, owner_id: str) -> List[Vehicle]:
        """Lista veículos por dono (via store)"""
        # TODO: Implementar quando tivermos relação Store -> Owner
        return []

    async def list_all(self, limit: int = 100) -> List[Vehicle]:
        models = self._session.query(VehicleModel)\
            .order_by(VehicleModel.created_at.desc())\
            .limit(limit)\
            .all()
        
        return [model.to_domain() for model in models]

    async def list_by_store(self, store_id: str) -> List[Vehicle]:
        try:
            store_uuid = UUID(store_id)
        except ValueError:
            return []
            
        models = self._session.query(VehicleModel)\
            .filter(VehicleModel.store_id == store_uuid)\
            .order_by(VehicleModel.created_at.desc())\
            .all()
        
        return [model.to_domain() for model in models]

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
        """Filtra veículos por critérios específicos"""
        query = self._session.query(VehicleModel)
        
        # Aplica filtros
        if brand:
            query = query.filter(VehicleModel.brand == brand.value)
        if vehicle_type:
            query = query.filter(VehicleModel.vehicle_type == vehicle_type.value)
        if condition:
            query = query.filter(VehicleModel.condition == condition.value)
        if min_price is not None:
            query = query.filter(VehicleModel.price >= min_price)
        if max_price is not None:
            query = query.filter(VehicleModel.price <= max_price)
        if store_id:
            try:
                store_uuid = UUID(store_id)
                query = query.filter(VehicleModel.store_id == store_uuid)
            except ValueError:
                pass
        if implement_segment:
            query = query.filter(VehicleModel.implement_segment == implement_segment)
        
        models = query.order_by(VehicleModel.created_at.desc()).all()
        return [model.to_domain() for model in models]

    async def search_vehicles(self, query: str) -> List[Vehicle]:
        search_term = f"%{query}%"
        models = self._session.query(VehicleModel)\
            .filter(
                VehicleModel.model.ilike(search_term) |
                VehicleModel.description.ilike(search_term)
            )\
            .order_by(VehicleModel.created_at.desc())\
            .all()
        
        return [model.to_domain() for model in models]

    async def count_by_store(self, store_id: str) -> int:
        try:
            store_uuid = UUID(store_id)
        except ValueError:
            return 0
            
        count = self._session.query(VehicleModel)\
            .filter(VehicleModel.store_id == store_uuid)\
            .count()
        
        return count

    # --- MÉTODO DE COMPATIBILIDADE ---
    async def get_by_plate(self, plate: str) -> Optional[Vehicle]:
        model = self._session.query(VehicleModel)\
            .filter(VehicleModel.plate == plate.upper().strip())\
            .first()
        return model.to_domain() if model else None