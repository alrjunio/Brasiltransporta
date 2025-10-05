import pytest
from unittest.mock import Mock, patch
from brasiltransporta.domain.errors.errors import ValidationError

class TestAdvertisementRoutes:
    
    @pytest.mark.skip(reason="Needs controller factory functions implementation")
    def test_create_advertisement_success(self, client):
        """Testa criação bem-sucedida de anúncio via API"""
        with patch('brasiltransporta.presentation.api.controllers.advertisements.get_create_advertisement_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.return_value = Mock(advertisement_id="ad-123")
            mock_uc.return_value = mock_use_case
            
            payload = {
                "store_id": "store-123",
                "vehicle_id": "vehicle-456", 
                "title": "Caminhão Volvo 2022",
                "description": "Caminhão em excelente estado",
                "price_amount": 150000.00
            }
            
            response = client.post("/advertisements", json=payload)
            
            assert response.status_code == 201
            assert response.json()["advertisement_id"] == "ad-123"
            mock_use_case.execute.assert_called_once()
    
    @pytest.mark.skip(reason="Needs controller factory functions implementation")
    def test_create_advertisement_validation_error(self, client):
        """Testa criação de anúncio com erro de validação"""
        with patch('brasiltransporta.presentation.api.controllers.advertisements.get_create_advertisement_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.side_effect = ValidationError("Loja não encontrada")
            mock_uc.return_value = mock_use_case
            
            payload = {
                "store_id": "store-invalid",
                "vehicle_id": "vehicle-456",
                "title": "Caminhão Volvo 2022", 
                "description": "Caminhão em excelente estado",
                "price_amount": 150000.00
            }
            
            response = client.post("/advertisements", json=payload)
            
            assert response.status_code == 400
            assert "Loja não encontrada" in response.json()["detail"]
    
    @pytest.mark.skip(reason="Needs controller factory functions implementation")
    def test_get_advertisement_success(self, client):
        """Testa busca bem-sucedida de anúncio via API"""
        with patch('brasiltransporta.presentation.api.controllers.advertisements.get_get_advertisement_by_id_uc') as mock_uc:
            mock_use_case = Mock()
            mock_ad = Mock()
            mock_ad.id = "ad-123"
            mock_ad.title = "Caminhão Volvo 2022"
            mock_ad.description = "Caminhão em excelente estado"
            mock_ad.price_amount = 150000.00
            mock_ad.status = "draft"
            mock_use_case.execute.return_value = mock_ad
            mock_uc.return_value = mock_use_case
            
            response = client.get("/advertisements/ad-123")
            
            assert response.status_code == 200
            assert response.json()["id"] == "ad-123"
            assert response.json()["title"] == "Caminhão Volvo 2022"
    
    @pytest.mark.skip(reason="Needs controller factory functions implementation")
    def test_get_advertisement_not_found(self, client):
        """Testa busca de anúncio não encontrado via API"""
        with patch('brasiltransporta.presentation.api.controllers.advertisements.get_get_advertisement_by_id_uc') as mock_uc:
            mock_use_case = Mock()
            mock_use_case.execute.side_effect = ValidationError("Anúncio não encontrado")
            mock_uc.return_value = mock_use_case
            
            response = client.get("/advertisements/ad-not-found")
            
            assert response.status_code == 404
            assert "Anúncio não encontrado" in response.json()["detail"]


class TestPlanRoutes:
    
    @pytest.mark.skip(reason="FastAPI dependency caching issue - will refactor to service-level testing")
    def test_create_plan_success(self, client):
        """Testa criação bem-sucedida de plano via API"""
        pass

    @pytest.mark.skip(reason="FastAPI dependency caching issue - will refactor to service-level testing")
    def test_list_plans_success(self, client):
        """Testa listagem bem-sucedida de planos via API"""
        pass

class TestTransactionRoutes:
    
    @pytest.mark.skip(reason="FastAPI dependency caching issue - will refactor to service-level testing")
    def test_create_transaction_success(self, client):
        """Testa criação bem-sucedida de transação via API"""
        pass
    
    @pytest.mark.skip(reason="FastAPI dependency caching issue - will refactor to service-level testing")
    def test_create_transaction_validation_error(self, client):
        """Testa criação de transação com erro de validação"""
        pass
    
    @pytest.mark.skip(reason="FastAPI dependency caching issue - will refactor to service-level testing")
    def test_get_transaction_success(self, client):
        """Testa busca bem-sucedida de transação via API"""
        pass
    
    @pytest.mark.skip(reason="FastAPI dependency caching issue - will refactor to service-level testing")
    def test_get_transaction_not_found(self, client):
        """Testa busca de transação não encontrada via API"""
        pass