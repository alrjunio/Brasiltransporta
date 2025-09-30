# tests/presentation/api/test_routes.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from brasiltransporta.main import app

class TestAdvertisementRoutes:
    def test_create_advertisement_success(self, client):
        """Testa criação bem-sucedida de anúncio via API"""
        with patch('brasiltransporta.presentation.api.routes.advertisements.get_create_advertisement_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(advertisement_id="adv-123")
            mock_uc.return_value = mock_use_case
            
            payload = {
                "store_id": "store-123",
                "vehicle_id": "vehicle-456",
                "title": "Caminhão Volvo 2022",
                "description": "Caminhão em excelente estado, revisado",
                "price_amount": 150000.00,
                "price_currency": "BRL"
            }
            
            response = client.post("/advertisements", json=payload)
            
            assert response.status_code == 201
            assert response.json()["id"] == "adv-123"

    def test_create_advertisement_validation_error(self, client):
        """Testa criação de anúncio com erro de validação"""
        with patch('brasiltransporta.presentation.api.routes.advertisements.get_create_advertisement_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.side_effect = Exception("Erro de validação")
            mock_uc.return_value = mock_use_case
            
            payload = {
                "store_id": "store-123",
                "vehicle_id": "vehicle-456",
                "title": "Cam",  # Título muito curto
                "description": "Descrição válida",
                "price_amount": 150000.00
            }
            
            response = client.post("/advertisements", json=payload)
            
            assert response.status_code == 422

    def test_get_advertisement_success(self, client):
        """Testa busca bem-sucedida de anúncio via API"""
        with patch('brasiltransporta.presentation.api.routes.advertisements.get_get_advertisement_by_id_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(
                id="adv-123",
                store_id="store-123",
                vehicle_id="vehicle-456",
                title="Caminhão Volvo 2022",
                description="Caminhão em excelente estado",
                price_amount=150000.00,
                price_currency="BRL",
                status="draft",
                is_featured=False,
                views=0,
                created_at="2023-01-01T00:00:00",
                updated_at="2023-01-01T00:00:00"
            )
            mock_uc.return_value = mock_use_case
            
            response = client.get("/advertisements/adv-123")
            
            assert response.status_code == 200
            assert response.json()["id"] == "adv-123"
            assert response.json()["title"] == "Caminhão Volvo 2022"

    def test_get_advertisement_not_found(self, client):
        """Testa busca de anúncio não encontrado via API"""
        with patch('brasiltransporta.presentation.api.routes.advertisements.get_get_advertisement_by_id_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = None
            mock_uc.return_value = mock_use_case
            
            response = client.get("/advertisements/non-existent-id")
            
            assert response.status_code == 404

class TestPlanRoutes:
    def test_create_plan_success(self, client):
        """Testa criação bem-sucedida de plano via API"""
        with patch('brasiltransporta.presentation.api.routes.plans.get_create_plan_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(plan_id="plan-123")
            mock_uc.return_value = mock_use_case
            
            payload = {
                "name": "Plano Básico",
                "description": "Plano ideal para pequenas empresas",
                "plan_type": "basic",
                "billing_cycle": "monthly",
                "price_amount": 199.90,
                "max_ads": 10,
                "max_featured_ads": 1,
                "features": ["Suporte por email", "5 anúncios ativos"]
            }
            
            response = client.post("/plans", json=payload)
            
            assert response.status_code == 201
            assert response.json()["id"] == "plan-123"

    def test_list_plans_success(self, client):
        """Testa listagem bem-sucedida de planos via API"""
        with patch('brasiltransporta.presentation.api.routes.plans.get_list_active_plans_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(plans=[
                Mock(
                    id="plan-1",
                    name="Plano Básico",
                    description="Plano básico",
                    plan_type="basic",
                    billing_cycle="monthly",
                    price_amount=199.90,
                    price_currency="BRL",
                    max_ads=10,
                    max_featured_ads=1,
                    features=["Feature 1"]
                ),
                Mock(
                    id="plan-2",
                    name="Plano Premium",
                    description="Plano premium",
                    plan_type="premium",
                    billing_cycle="monthly",
                    price_amount=499.90,
                    price_currency="BRL",
                    max_ads=50,
                    max_featured_ads=5,
                    features=["Feature 1", "Feature 2"]
                )
            ])
            mock_uc.return_value = mock_use_case
            
            response = client.get("/plans")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["plans"]) == 2
            assert data["plans"][0]["name"] == "Plano Básico"
            assert data["plans"][1]["name"] == "Plano Premium"

class TestTransactionRoutes:
    def test_create_transaction_success(self, client):
        """Testa criação bem-sucedida de transação via API"""
        with patch('brasiltransporta.presentation.api.routes.transactions.get_create_transaction_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(transaction_id="trans-123")
            mock_uc.return_value = mock_use_case
            
            payload = {
                "user_id": "user-123",
                "plan_id": "plan-456",
                "amount": 199.90,
                "payment_method": "credit_card",
                "currency": "BRL",
                "metadata": {"card_last_digits": "1234"}
            }
            
            response = client.post("/transactions", json=payload)
            
            assert response.status_code == 201
            assert response.json()["id"] == "trans-123"

@pytest.fixture
def client():
    """Fixture para cliente de teste FastAPI"""
    return TestClient(app)
