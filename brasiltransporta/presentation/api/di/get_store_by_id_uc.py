from brasiltransporta.application.stores.use_cases.get_store_by_id import GetStoreByIdUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.store_repository import SQLAlchemyStoreRepository

def get_store_by_id_uc() -> GetStoreByIdUseCase:
    s = get_session()
    repo = SQLAlchemyStoreRepository(s)
    return GetStoreByIdUseCase(store_repo=repo, session=s)