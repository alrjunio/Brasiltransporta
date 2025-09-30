from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from brasiltransporta.domain.entities.vehicle import Vehicle
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.vehicle import VehicleModel

class SQLAlchemyVehicleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, vehicle: Vehicle) -> None:
        v = VehicleModel(
            id=UUID(vehicle.id),
            store_id=UUID(vehicle.store_id),
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            plate=vehicle.plate,
        )
        self._session.add(v)
        self._session.flush()
        self._session.commit()

    def get_by_id(self, vehicle_id: UUID) -> Optional[Vehicle]:
        model = self._session.get(VehicleModel, vehicle_id)
        if not model:
            return None
        return Vehicle(
            id=str(model.id),
            store_id=str(model.store_id),
            brand=model.brand,
            model=model.model,
            year=model.year,
            plate=model.plate,
        )

    def get_by_plate(self, plate: str) -> Optional[Vehicle]:
        model = self._session.query(VehicleModel).filter(VehicleModel.plate == plate.upper().strip()).first()
        if not model:
            return None
        return Vehicle(
            id=str(model.id),
            store_id=str(model.store_id),
            brand=model.brand,
            model=model.model,
            year=model.year,
            plate=model.plate,
        )

    def list_by_store(self, store_id: UUID, limit: int = 50, offset: int = 0) -> List[Vehicle]:
        models = self._session.query(VehicleModel)\
            .filter(VehicleModel.store_id == store_id)\
            .order_by(VehicleModel.created_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        return [
            Vehicle(
                id=str(model.id),
                store_id=str(model.store_id),
                brand=model.brand,
                model=model.model,
                year=model.year,
                plate=model.plate,
            )
            for model in models
        ]
