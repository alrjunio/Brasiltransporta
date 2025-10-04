# tests/conftest.py
import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base do seu projeto
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base

# FastAPI (se existir)
try:
    from fastapi.testclient import TestClient
    from brasiltransporta.presentation.api.app import app
    HAS_API = True
except Exception:
    HAS_API = False
    app = None
    TestClient = None

# URL do banco de testes: usa o Postgres do docker-compose
DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@postgres_db:5432/brasiltransporta")
)

@pytest.fixture(scope="session")
def engine():
    eng = create_engine(DATABASE_URL, future=True)
    # cria todas as tabelas 1x por sessão de testes
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()

@pytest.fixture(scope="function")
def db_session(engine):
    """Sessão nova por teste, com rollback no final."""
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    """Cliente FastAPI, injetando a sessão de teste na app."""
    if not HAS_API:
        pytest.skip("App FastAPI nao disponivel.")

    # sua função original de sessão
    from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session as _get_session

    def _test_session():
        try:
            yield db_session
        finally:
            pass

    monkeypatch.setattr(
        "brasiltransporta.infrastructure.persistence.sqlalchemy.session.get_session",
        _test_session,
        raising=True,
    )

    return TestClient(app)
