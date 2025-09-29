from dataclasses import dataclass
from typing import Protocol
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.repositories.user_repository import UserRepository


class PasswordHasher(Protocol):
    def hash(self, raw_password: str) -> str: ...


@dataclass(frozen=True)
class RegisterUserInput:
    name: str
    email: str
    password: str
    phone: str | None = None
    birth_date: str | None = None
    profession: str | None = None
    region: str | None = None


@dataclass(frozen=True)
class RegisterUserOutput:
    user_id: str


class RegisterUserUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, data: RegisterUserInput) -> RegisterUserOutput:
        # 1) regra de idempotência por email
        existing = self._users.get_by_email(data.email)
        if existing:
            return RegisterUserOutput(user_id=existing.id)

        # 2) orquestração de infraestrutura: gerar hash da senha
        pwd_hash = self._hasher.hash(data.password)

        # 3) criar entidade de domínio (invariantes validadas lá)
        user = User.create(
            name=data.name,
            email=data.email,
            password_hash=pwd_hash,
            phone=data.phone,
            birth_date=data.birth_date,
            profession=data.profession,
            region=data.region,
        )

        # 4) persistir via contrato de repositório
        self._users.add(user)

        # 5) retornar DTO de saída
        return RegisterUserOutput(user_id=user.id)
