from brasiltransporta.application.vehicles.use_cases.create_vehicle import CreateVehicleUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories import SQLAlchemyVehicleRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session

def get_create_vehicle_uc():
    s = get_session()
    repo = SQLAlchemyVehicleRepository(s)
    return CreateVehicleUseCase(repo)
