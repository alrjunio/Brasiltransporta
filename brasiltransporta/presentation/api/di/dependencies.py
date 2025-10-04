from fastapi import Depends
from sqlalchemy.orm import Session

from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.advertisement_repository import SQLAlchemyAdvertisementRepository
from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementUseCase
from brasiltransporta.application.advertisements.use_cases.get_advertisement_by_id import GetAdvertisementByIdUseCase
from brasiltransporta.application.advertisements.use_cases.publish_advertisement import PublishAdvertisementUseCase

# Provider do repositório (já existe no get_advertisement_repo.py)
def get_advertisement_repo(db: Session = Depends(get_session)) -> SQLAlchemyAdvertisementRepository:
    return SQLAlchemyAdvertisementRepository(db)

# Providers dos use cases
def get_create_advertisement_uc(
    repo: SQLAlchemyAdvertisementRepository = Depends(get_advertisement_repo)
) -> CreateAdvertisementUseCase:
    # Para testes, podemos passar None para store_repo e vehicle_repo temporariamente
    return CreateAdvertisementUseCase(repo, None, None)

def get_get_advertisement_by_id_uc(
    repo: SQLAlchemyAdvertisementRepository = Depends(get_advertisement_repo)
) -> GetAdvertisementByIdUseCase:
    return GetAdvertisementByIdUseCase(repo)

def get_publish_advertisement_uc(
    repo: SQLAlchemyAdvertisementRepository = Depends(get_advertisement_repo)
) -> PublishAdvertisementUseCase:
    return PublishAdvertisementUseCase(repo)