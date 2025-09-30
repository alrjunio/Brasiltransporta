# presentation/api/di/providers.py
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.advertisement_repository import SQLAlchemyAdvertisementRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.plan_repository import SQLAlchemyPlanRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.transaction_repository import SQLAlchemyTransactionRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.store_repository import SQLAlchemyStoreRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.vehicle_repository import SQLAlchemyVehicleRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository

# Advertisement Use Cases
def get_create_advertisement_uc():
    session = get_session()
    ad_repo = SQLAlchemyAdvertisementRepository(session)
    store_repo = SQLAlchemyStoreRepository(session)
    vehicle_repo = SQLAlchemyVehicleRepository(session)
    from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementUseCase
    return CreateAdvertisementUseCase(ad_repo, store_repo, vehicle_repo)

def get_get_advertisement_by_id_uc():
    session = get_session()
    ad_repo = SQLAlchemyAdvertisementRepository(session)
    from brasiltransporta.application.advertisements.use_cases.get_advertisement_by_id import GetAdvertisementByIdUseCase
    return GetAdvertisementByIdUseCase(ad_repo)

def get_publish_advertisement_uc():
    session = get_session()
    ad_repo = SQLAlchemyAdvertisementRepository(session)
    from brasiltransporta.application.advertisements.use_cases.publish_advertisement import PublishAdvertisementUseCase
    return PublishAdvertisementUseCase(ad_repo)

# Plan Use Cases
def get_create_plan_uc():
    session = get_session()
    plan_repo = SQLAlchemyPlanRepository(session)
    from brasiltransporta.application.plans.use_cases.create_plan import CreatePlanUseCase
    return CreatePlanUseCase(plan_repo)

def get_get_plan_by_id_uc():
    session = get_session()
    plan_repo = SQLAlchemyPlanRepository(session)
    from brasiltransporta.application.plans.use_cases.get_plan_by_id import GetPlanByIdUseCase
    return GetPlanByIdUseCase(plan_repo)

def get_list_active_plans_uc():
    session = get_session()
    plan_repo = SQLAlchemyPlanRepository(session)
    from brasiltransporta.application.plans.use_cases.list_active_plans import ListActivePlansUseCase
    return ListActivePlansUseCase(plan_repo)

# Transaction Use Cases
def get_create_transaction_uc():
    session = get_session()
    transaction_repo = SQLAlchemyTransactionRepository(session)
    user_repo = SQLAlchemyUserRepository(session)
    plan_repo = SQLAlchemyPlanRepository(session)
    from brasiltransporta.application.transactions.use_cases.create_transaction import CreateTransactionUseCase
    return CreateTransactionUseCase(transaction_repo, user_repo, plan_repo)

def get_get_transaction_by_id_uc():
    session = get_session()
    transaction_repo = SQLAlchemyTransactionRepository(session)
    from brasiltransporta.application.transactions.use_cases.get_transaction_by_id import GetTransactionByIdUseCase
    return GetTransactionByIdUseCase(transaction_repo)
