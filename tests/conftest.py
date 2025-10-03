# tests/conftest.py
import pytest
from brasiltransporta.presentation.api.app import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Fixture para cliente de teste FastAPI"""
    return TestClient(app)

# Fixtures para Advertisement
@pytest.fixture
def sample_advertisement_data():
    return {
        "store_id": "store-123",
        "vehicle_id": "vehicle-456", 
        "title": "Caminhão Volvo 2022",
        "description": "Caminhão em excelente estado",
        "price_amount": 150000.00
    }

# Fixtures para Plan
@pytest.fixture  
def sample_plan_data():
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

# Fixtures para Transaction
@pytest.fixture
def sample_transaction_data():
    return {
        "user_id": "user-123",
        "plan_id": "plan-456", 
        "amount": 199.90,
        "payment_method": "credit_card",
        "metadata": {"card_last_digits": "1234"}
    }