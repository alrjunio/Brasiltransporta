from dataclasses import dataclass
from typing import Optional, List, Dict

import pytest

from brasiltransporta.application.users.use_cases.register_user import (
    RegisterUserUseCase,
    RegisterUserInput,
)
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.errors.errors import ValidationError


# ---- Fakes de teste ----

class FakePasswordHasher:
    def hash(self, raw_password: str) -> str:
        # não usa passlib/bcrypt nos testes unitários
        return f"hash::{raw_password}"


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._by_id: Dict[str, User] = {}
        self._by_email: Dict[str, User] = {}

    def add(self, user: User) -> None:
        self._by_id[user.id] = user
        self._by_email[str(user.email).lower()] = user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._by_id.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self._by_email.get(email.lower())

    def list_by_region(self, region: str, limit: int = 50) -> List[User]:
        return [u for u in self._by_id.values() if (u.region == region)][:limit]


# ---- Tests ----

def test_register_user_success():
    repo = InMemoryUserRepository()
    hasher = FakePasswordHasher()
    uc = RegisterUserUseCase(users=repo, hasher=hasher)

    out = uc.execute(
        RegisterUserInput(
            name="Ana",
            email="ana@example.com",
            password="segredo123",
            region="Sudeste",
        )
    )

    assert isinstance(out.user_id, str)
    saved = repo.get_by_id(out.user_id)
    assert saved is not None
    assert str(saved.email) == "ana@example.com"
    assert saved.region == "Sudeste"


def test_register_user_duplicate_email_raises_validation_error():
    repo = InMemoryUserRepository()
    hasher = FakePasswordHasher()
    uc = RegisterUserUseCase(users=repo, hasher=hasher)

    # primeiro cadastro
    uc.execute(
        RegisterUserInput(
            name="Ana",
            email="ana@example.com",
            password="segredo123",
            region="Sudeste",
        )
    )

    # duplicado deve lançar ValidationError
    with pytest.raises(ValidationError):
        uc.execute(
            RegisterUserInput(
                name="Ana 2",
                email="ana@example.com",
                password="outra",
                region="Sudeste",
            )
        )
