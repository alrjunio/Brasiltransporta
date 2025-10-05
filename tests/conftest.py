# tests/conftest.py
import os
import pytest
from unittest.mock import Mock, MagicMock

# FastAPI (se existir)
try:
    from fastapi.testclient import TestClient
    from brasiltransporta.presentation.api.app import app
    HAS_API = True
except Exception:
    HAS_API = False
    app = None
    TestClient = None

@pytest.fixture(scope="session")
def engine():
    """Mock engine para evitar conexão com banco real"""
    mock_engine = Mock()
    return mock_engine

@pytest.fixture(scope="function")
def db_session(engine):
    """Mock session para evitar conexão com banco real"""
    mock_session = Mock()
    # Configurar comportamentos básicos do mock
    mock_session.commit = Mock()
    mock_session.rollback = Mock() 
    mock_session.close = Mock()
    mock_session.execute = Mock(return_value=Mock(scalar=Mock(return_value=None)))
    return mock_session

@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    """Cliente FastAPI com mocks para evitar banco real"""
    if not HAS_API:
        pytest.skip("App FastAPI não disponível.")

    # Mock da função get_session para retornar nossa session mockada
    def _mock_session():
        yield db_session

    monkeypatch.setattr(
        "brasiltransporta.infrastructure.persistence.sqlalchemy.session.get_session",
        _mock_session,
        raising=True,
    )

    # Mock de qualquer outra dependência de banco que possa existir
    monkeypatch.setattr(
        "brasiltransporta.infrastructure.persistence.sqlalchemy.models.base.Base.metadata.create_all",
        Mock(),
        raising=True,
    )

    return TestClient(app)
