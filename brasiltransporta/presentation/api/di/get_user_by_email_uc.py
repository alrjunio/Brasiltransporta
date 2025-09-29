from brasiltransporta.application.users.use_cases.get_user_by_email import GetUserByEmailUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session


def get_user_by_email_uc() -> GetUserByEmailUseCase:
    session = get_session()
    repo = SQLAlchemyUserRepository(session)
    return GetUserByEmailUseCase(users=repo)
