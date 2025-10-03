from typing import Optional, List, Dict

from brasiltransporta.application.users.use_cases.get_user_by_id import (
    GetUserByIdUseCase,
    GetUserByIdOutput,
)
from brasiltransporta.application.users.use_cases.get_user_by_email import (
    GetUserByEmailUseCase,
)
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.domain.entities.user import User


# ----- Fake InMemory Repo (somente para testes unitários) -----

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
        return [u for u in self._by_id.values() if u.region == region][:limit]


# ----- Builders helpers -----

def make_user(name="Ana", email="ana@example.com", region="Sudeste") -> User:
    # password_hash arbitrário para testes unitários (sem bcrypt/passlib aqui)
    return User.create(
        name=name,
        email=email,
        password_hash="hash::teste",
        phone=None,
        birth_date=None,
        profession=None,
        region=region,
    )


# ----- Tests: GetUserById -----

def test_get_user_by_id_found():
    repo = InMemoryUserRepository()
    u = make_user()
    repo.add(u)

    uc = GetUserByIdUseCase(users=repo)
    out = uc.execute(u.id)

    assert isinstance(out, GetUserByIdOutput)
    assert out.id == u.id
    assert out.email == "ana@example.com"
    assert out.name == "Ana"
    assert out.region == "Sudeste"


def test_get_user_by_id_not_found_returns_none():
    repo = InMemoryUserRepository()
    uc = GetUserByIdUseCase(users=repo)

    out = uc.execute("nao-existe")
    assert out is None


# ----- Tests: GetUserByEmail -----

def test_get_user_by_email_found():
    repo = InMemoryUserRepository()
    u = make_user(name="Bia", email="bia@example.com", region="Sul")
    repo.add(u)

    uc = GetUserByEmailUseCase(users=repo)
    out = uc.execute("bia@example.com")

    assert isinstance(out, GetUserByIdOutput)  # mesmo DTO
    assert out.id == u.id
    assert out.name == "Bia"
    assert out.email == "bia@example.com"
    assert out.region == "Sul"


def test_get_user_by_email_not_found_returns_none():
    repo = InMemoryUserRepository()
    uc = GetUserByEmailUseCase(users=repo)

    out = uc.execute("x@example.com")
    assert out is None
