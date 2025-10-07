from brasiltransporta.application.users.use_cases.login_user import LoginUserUseCase
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository
from brasiltransporta.infrastructure.security.password_hasher import BcryptPasswordHasher
from brasiltransporta.infrastructure.security.jwt_service import JWTService

def get_login_user_uc() -> LoginUserUseCase:
    """Provider para LoginUserUseCase"""
    session = get_session()
    repo = SQLAlchemyUserRepository(session)
    hasher = BcryptPasswordHasher()
    jwt_service = JWTService()
    return LoginUserUseCase(users=repo, hasher=hasher, jwt_service=jwt_service)