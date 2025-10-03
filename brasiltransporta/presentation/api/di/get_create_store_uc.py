from brasiltransporta.application.stores.use_cases.create_store import CreateStoreUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.store_repository import SQLAlchemyStoreRepository

def get_create_store_uc() -> CreateStoreUseCase:
    s = get_session()
    repo = SQLAlchemyStoreRepository(s)
    return CreateStoreUseCase(stores=repo)