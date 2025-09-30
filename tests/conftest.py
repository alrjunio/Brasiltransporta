# tests/conftest.py
import pytest
import asyncio
from typing import Generator
from unittest.mock import Mock

from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session
from brasiltransporta.main import app

# Configurações globais para testes
pytest_plugins = []

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Fixture para event loop assíncrono"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_session():
    """Fixture para sessão mock do banco de dados"""
    session = Mock()
    return session

@pytest.fixture
def sample_user_data():
    """Fixture com dados de exemplo para usuário"""
    return {
        "name": "João Silva",
        "email": "joao@email.com",
        "password": "senha123",
        "phone": "+5511999999999",
        "region": "Sudeste"
    }

@pytest.fixture
def sample_store_data():
    """Fixture com dados de exemplo para loja"""
    return {
        "name": "Minha Loja de Caminhões",
        "owner_user_id": "user-123"
    }

@pytest.fixture
def sample_vehicle_data():
    """Fixture com dados de exemplo para veículo"""
    return {
        "store_id": "store-123",
        "brand": "Volvo",
        "model": "FH 540",
        "year": 2022,
        "plate": "ABC1234"
    }

@pytest.fixture
def sample_advertisement_data():
    """Fixture com dados de exemplo para anúncio"""
    return {
        "store_id": "store-123",
        "vehicle_id": "vehicle-456",
        "title": "Caminhão Volvo 2022",
        "description": "Caminhão em excelente estado, revisado",
        "price_amount": 150000.00
    }

@pytest.fixture
def sample_plan_data():
    """Fixture com dados de exemplo para plano"""
    return {
        "name": "Plano Básico",
        "description": "Plano ideal para pequenas empresas",
        "plan_type": "basic",
        "billing_cycle": "monthly",
        "price_amount": 199.90,
        "max_ads": 10,
        "max_featured_ads": 1,
        "features": ["Suporte por email", "5 anúncios ativos"]
    }

@pytest.fixture
def sample_transaction_data():
    """Fixture com dados de exemplo para transação"""
    return {
        "user_id": "user-123",
        "plan_id": "plan-456",
        "amount": 199.90,
        "payment_method": "credit_card",
        "metadata": {"card_last_digits": "1234"}
    }
