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


def get_register_user_uc() -> RegisterUserUseCase:
    """
    Provider simples para FastAPI/Depends:
    cria sessão, repo concreto e o hasher real, e devolve o caso de uso.
    """
    session = get_session()
    repo = SQLAlchemyUserRepository(session)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(users=repo, hasher=hasher)


from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository