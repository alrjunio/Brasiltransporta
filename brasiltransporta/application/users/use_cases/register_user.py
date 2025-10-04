from dataclasses import dataclass
from typing import Optional

from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.errors.errors import ValidationError


class PasswordHasher:
    def hash(self, raw_password: str) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class RegisterUserInput:
    name: str
    email: str
    password: str
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    profession: Optional[str] = None
    region: Optional[str] = None


@dataclass(frozen=True)
class RegisterUserOutput:
    user_id: str


class RegisterUserUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, data: RegisterUserInput) -> RegisterUserOutput:
        # Regra: e-mail já existe? -> 422
        existing = self._users.get_by_email(data.email)
        if existing:
            raise ValidationError("E-mail já cadastrado.")

        pwd_hash = self._hasher.hash(data.password)

        user = User.create(
            name=data.name,
            email=data.email,
            password_hash=pwd_hash,
            phone=data.phone,
            birth_date=data.birth_date,
            profession=data.profession,
            region=data.region,
        )

        self._users.add(user)
        return RegisterUserOutput(user_id=user.id)
