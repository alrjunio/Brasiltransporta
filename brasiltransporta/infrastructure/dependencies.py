# brasiltransporta/infrastructure/dependencies.py
from fastapi import Request, HTTPException, status, Depends
from typing import Optional

from brasiltransporta.infrastructure.security.refresh_token_service import RefreshTokenService
from brasiltransporta.application.service.user_service import UserService
from brasiltransporta.infrastructure.security.jwt_service import JWTService
from brasiltransporta.infrastructure.security.password_hasher import BcryptPasswordHasher

from brasiltransporta.infrastructure.external.sms.sms_service import SMSService, MockSMSService

from brasiltransporta.domain.repositories.phone_verification_repository import PhoneVerificationRepository
from brasiltransporta.domain.repositories.user_repository import UserRepository

# Import dos Use Cases
from brasiltransporta.application.auth.use_case.phone_auth_use_cases import SendPhoneVerificationUseCase, VerifyPhoneCodeUseCase
from brasiltransporta.application.auth.use_case.phone_login_use_case import PhoneLoginUseCase

# Import do repositório REAL
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository

# Import do Redis Repository (vamos criar)
from brasiltransporta.infrastructure.persistence.redis.phone_verification_repository_impl import RedisPhoneVerificationRepository

# Tentar importar a sessão do banco
try:
    from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session as get_db_session
except ImportError:
    try:
        from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session as get_db_session
    except ImportError:
        # Fallback temporário
        def get_db_session():
            raise Exception("Sessão do banco não configurada")

def get_refresh_token_service(request: Request) -> Optional[RefreshTokenService]:
    """Dependency to get RefreshTokenService from app state"""
    refresh_service = getattr(request.app.state, 'refresh_token_service', None)
    
    if refresh_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Refresh token service unavailable"
        )
    
    return refresh_service

def get_jwt_service() -> JWTService:
    """Dependency para JWTService"""
    return JWTService()

def get_password_hasher() -> BcryptPasswordHasher:
    """Dependency para PasswordHasher"""
    return BcryptPasswordHasher()

def get_user_repository() -> UserRepository:
    """Dependency para UserRepository real"""
    try:
        session = get_db_session()
        return SQLAlchemyUserRepository(session)
    except Exception as e:
        print(f"❌ Erro ao criar UserRepository: {e}")
        # Fallback para mock se não conseguir conectar ao banco
        return MockUserRepository()

def get_user_service() -> UserService:
    """Dependency injection para UserService com repositório REAL"""
    print("🔧 Inicializando UserService com repositório PostgreSQL REAL...")
    
    user_repo = get_user_repository()
    hasher = get_password_hasher()
    jwt_service = get_jwt_service()
    
    return UserService(
        user_repository=user_repo,
        password_hasher=hasher, 
        jwt_service=jwt_service
    )

# Dependências para Phone Auth
def get_phone_verification_repository() -> PhoneVerificationRepository:
    """Dependency para PhoneVerificationRepository com Redis"""
    return RedisPhoneVerificationRepository()

def get_sms_service() -> SMSService:
    """Dependency para SMSService (Mock em desenvolvimento)"""
    return MockSMSService()

def get_send_phone_verification_use_case() -> SendPhoneVerificationUseCase:
    """Dependency para SendPhoneVerificationUseCase"""
    return SendPhoneVerificationUseCase(
        verification_repo=get_phone_verification_repository(),
        sms_service=get_sms_service()
    )

def get_verify_phone_code_use_case() -> VerifyPhoneCodeUseCase:
    """Dependency para VerifyPhoneCodeUseCase"""
    return VerifyPhoneCodeUseCase(
        verification_repo=get_phone_verification_repository(),
        user_repo=get_user_repository()
    )

def get_phone_login_use_case() -> PhoneLoginUseCase:
    """Dependency para PhoneLoginUseCase"""
    return PhoneLoginUseCase(
        verification_repo=get_phone_verification_repository(),
        user_repo=get_user_repository(),
        jwt_service=get_jwt_service() 
    )

# Manter o MockUserRepository como fallback
class MockUserRepository:
    def get_by_email(self, email):
        print(f"🔍 MockUserRepository: buscando usuário por email: {email}")
        return None
    
    def get_by_id(self, user_id):
        print(f"🔍 MockUserRepository: buscando usuário por ID: {user_id}")
        return None
    
    def save(self, user):
        print(f"💾 MockUserRepository: salvando usuário: {user}")
        return user

    def find_by_phone(self, phone: str):
        print(f"🔍 MockUserRepository: buscando usuário por telefone: {phone}")
        return None