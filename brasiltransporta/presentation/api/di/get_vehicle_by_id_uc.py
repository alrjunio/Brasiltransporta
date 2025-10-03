from brasiltransporta.application.vehicles.use_cases.get_vehicle_by_id import GetVehicleByIdUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories import SQLAlchemyVehicleRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session

def get_vehicle_by_id_uc():
    s = get_session()
    repo = SQLAlchemyVehicleRepository(s)
    return GetVehicleByIdUseCase(repo)
