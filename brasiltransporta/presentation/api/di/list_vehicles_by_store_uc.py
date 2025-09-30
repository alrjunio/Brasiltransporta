from brasiltransporta.application.vehicles.use_cases.list_vehicles_by_store_uc import ListVehiclesByStoreUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories import SQLAlchemyVehicleRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session

def get_list_vehicles_by_store_uc():
    s = get_session()
    repo = SQLAlchemyVehicleRepository(s)
    return ListVehiclesByStoreUseCase(repo)
