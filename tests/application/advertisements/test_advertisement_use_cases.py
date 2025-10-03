# tests/application/advertisements/test_use_cases.py
import pytest
from unittest.mock import Mock, AsyncMock
from brasiltransporta.application.advertisements.use_cases.create_advertisement import (
    CreateAdvertisementUseCase, CreateAdvertisementInput
)
from brasiltransporta.application.advertisements.use_cases.get_advertisement_by_id import (
    GetAdvertisementByIdUseCase
)
from brasiltransporta.application.advertisements.use_cases.publish_advertisement import (
    PublishAdvertisementUseCase, PublishAdvertisementInput
)
from brasiltransporta.domain.entities.advertisement import Advertisement, AdvertisementStatus
from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.vehicle import Vehicle
from brasiltransporta.domain.errors import ValidationError

class TestCreateAdvertisementUseCase:
    def test_execute_success(self):
        """Testa criação bem-sucedida de anúncio"""
        # Mocks
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()
        
        # Setup
        store = Store.create("Minha Loja", "user-123")
        vehicle = Vehicle.create("store-123", "Volvo", "FH 540", 2022, "ABC1234")
        
        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = vehicle
        mock_ad_repo.add = Mock()
        
        # Use Case
        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        # Execute
        result = use_case.execute(input_data)
        
        # Assert
        assert result.advertisement_id is not None
        mock_store_repo.get_by_id.assert_called_once_with("store-123")
        mock_vehicle_repo.get_by_id.assert_called_once_with("vehicle-456")
        mock_ad_repo.add.assert_called_once()

    def test_execute_store_not_found(self):
        """Testa criação com loja não encontrada"""
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()
        
        mock_store_repo.get_by_id.return_value = None
        
        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        with pytest.raises(ValidationError, match="Loja não encontrada"):
            use_case.execute(input_data)

    def test_execute_vehicle_not_found(self):
        """Testa criação com veículo não encontrado"""
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()
        
        store = Store.create("Minha Loja", "user-123")
        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = None
        
        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        with pytest.raises(ValidationError, match="Veículo não encontrado"):
            use_case.execute(input_data)

class TestGetAdvertisementByIdUseCase:
    def test_execute_success(self):
        """Testa busca bem-sucedida de anúncio por ID"""
        mock_ad_repo = Mock()
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        mock_ad_repo.get_by_id.return_value = advertisement
        
        use_case = GetAdvertisementByIdUseCase(mock_ad_repo)
        result = use_case.execute(advertisement.id)
        
        assert result is not None
        assert result.id == advertisement.id
        assert result.title == "Caminhão Volvo 2022"
        mock_ad_repo.get_by_id.assert_called_once_with(advertisement.id)

    def test_execute_not_found(self):
        """Testa busca de anúncio não encontrado"""
        mock_ad_repo = Mock()
        mock_ad_repo.get_by_id.return_value = None
        
        use_case = GetAdvertisementByIdUseCase(mock_ad_repo)
        result = use_case.execute("non-existent-id")
        
        assert result is None

class TestPublishAdvertisementUseCase:
    def test_execute_success(self):
        """Testa publicação bem-sucedida de anúncio"""
        mock_ad_repo = Mock()
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        mock_ad_repo.get_by_id.return_value = advertisement
        mock_ad_repo.update = Mock()
        
        use_case = PublishAdvertisementUseCase(mock_ad_repo)
        input_data = PublishAdvertisementInput(advertisement_id=advertisement.id)
        
        result = use_case.execute(input_data)
        
        assert result.success == True
        assert advertisement.status == AdvertisementStatus.ACTIVE
        mock_ad_repo.update.assert_called_once_with(advertisement)

    def test_execute_advertisement_not_found(self):
        """Testa publicação de anúncio não encontrado"""
        mock_ad_repo = Mock()
        mock_ad_repo.get_by_id.return_value = None
        
        use_case = PublishAdvertisementUseCase(mock_ad_repo)
        input_data = PublishAdvertisementInput(advertisement_id="non-existent-id")
        
        with pytest.raises(ValidationError, match="Anúncio não encontrado"):
            use_case.execute(input_data)
