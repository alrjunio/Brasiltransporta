from dataclasses import dataclass
from typing import Optional
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.infrastructure.security.password_hasher import BcryptPasswordHasher
from brasiltransporta.infrastructure.security.jwt_service import JWTService
from brasiltransporta.domain.errors.errors import ValidationError

@dataclass(frozen=True)
class LoginUserInput:
    email: str
    password: str

@dataclass(frozen=True)
class LoginUserOutput:
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    name: str
    roles: list[str]
    token_type: str = "bearer"

class LoginUserUseCase:
    def __init__(
        self, 
        users: UserRepository, 
        hasher: BcryptPasswordHasher,
        jwt_service: JWTService
    ):
        self._users = users
        self._hasher = hasher
        self._jwt_service = jwt_service

    def execute(self, data: LoginUserInput) -> LoginUserOutput:
        # Buscar usuário por email
        user = self._users.get_by_email(data.email)
        if not user:
            raise ValidationError("Credenciais inválidas")

        # Verificar se usuário está ativo
        if not user.is_active:
            raise ValidationError("Conta desativada")

        # Verificar senha
        if not self._hasher.verify(data.password, user.password_hash):
            raise ValidationError("Credenciais inválidas")

        # Atualizar último login
        user.update_last_login()
        self._users.update(user)  # Será implementado na próxima correção

        # Gerar tokens JWT
        token_data = {"sub": user.id, "email": user.email, "roles": user.roles}
        
        access_token = self._jwt_service.create_access_token(token_data)
        refresh_token = self._jwt_service.create_refresh_token(token_data)

        return LoginUserOutput(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            name=user.name,
            roles=user.roles
        )
