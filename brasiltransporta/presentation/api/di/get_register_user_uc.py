from brasiltransporta.application.users.use_cases.register_user import (
    RegisterUserUseCase,
)
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from brasiltransporta.infrastructure.security.password_hasher import (
    BcryptPasswordHasher,
)

from brasiltransporta.application.users.use_cases.get_user_by_id import GetUserByIdUseCase

def get_register_user_uc() -> RegisterUserUseCase:
    """
    Provider simples para FastAPI/Depends:
    cria sessão, repo concreto e o hasher real, e devolve o caso de uso.
    """
    session = get_session()
    repo = SQLAlchemyUserRepository(session)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(users=repo, hasher=hasher)

def get_user_by_id_uc() -> GetUserByIdUseCase:
    session = get_session()
    repo = SQLAlchemyUserRepository(session)
    return GetUserByIdUseCase(users=repo)


