from brasiltransporta.application.users.use_cases.get_user_by_id import GetUserByIdUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session


def get_user_by_id_uc() -> GetUserByIdUseCase:
    session = get_session()
    repo = SQLAlchemyUserRepository(session)
    return GetUserByIdUseCase(users=repo)
