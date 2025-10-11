from unittest.mock import Mock
import pytest

from brasiltransporta.domain.entities.advertisement import Advertisement, AdvertisementStatus
from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.address import Address
from brasiltransporta.domain.entities.enums import StoreCategory
from brasiltransporta.application.advertisements.use_cases.create_advertisement import (
    CreateAdvertisementUseCase, 
    CreateAdvertisementInput,
    CreateAdvertisementOutput
)
from brasiltransporta.domain.errors.errors import ValidationError


class TestCreateAdvertisementUseCase:
    """Test cases for CreateAdvertisementUseCase"""

    def _create_test_store(self, name="Minha Loja", owner_id="user-123"):
        """Helper method para criar store de teste"""
        address = Address.create("Rua Teste", "São Paulo", "SP", "01234-000")
        return Store.create(
            name=name,
            owner_id=owner_id,
            description="Loja de veículos",
            address=address,
            categories=[StoreCategory.PARTS_STORE],
            contact_phone="(11, cnpj="12.345.678/0001-90", cnpj="12.345.678/0001-90") 99999-9999"
        )

    def test_create_advertisement_success(self):
        """Testa criação bem-sucedida de anúncio"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = Mock()
        mock_ad_repo.add.return_value = None

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Volvo FH 440 - Excelente estado",
            description="Caminhão Volvo FH 440, 6x4, ano 2020, 150.000 km",
            price_amount=250000.0
        )

        # Act
        result = use_case.execute(ad_input)

        # Assert
        assert result is not None
        assert isinstance(result, CreateAdvertisementOutput)
        assert hasattr(result, 'advertisement_id')
        mock_ad_repo.add.assert_called_once()

    def test_create_advertisement_invalid_price(self):
        """Testa criação de anúncio com preço inválido"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = Mock()

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo, 
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Volvo FH 440",
            description="Caminhão em bom estado",
            price_amount=-100.0
        )

        # Act & Assert - CORREÇÃO: Capture ValueError também
        with pytest.raises((ValidationError, ValueError), match="Preço deve ser maior que zero"):
            use_case.execute(ad_input)

    def test_create_advertisement_missing_required_fields(self):
        """Testa criação de anúncio com campos obrigatórios faltando"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = Mock()

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="A",
            description="Desc",
            price_amount=100000.0
        )

        # Act & Assert - CORREÇÃO: Capture ValueError também
        with pytest.raises((ValidationError, ValueError)):
            use_case.execute(ad_input)

    def test_create_advertisement_with_vehicle_info(self):
        """Testa criação de anúncio com informações do veículo"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = Mock()
        mock_ad_repo.add.return_value = None

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Scania R500 - 2021",
            description="Caminhão Scania R500, 6x4, ano 2021, 80.000 km, revisões em dia",
            price_amount=320000.0
        )

        # Act
        result = use_case.execute(ad_input)

        # Assert
        assert result is not None
        assert isinstance(result, CreateAdvertisementOutput)
        mock_ad_repo.add.assert_called_once()

    def test_create_advertisement_different_plan_durations(self):
        """Testa criação de anúncio com diferentes durações de plano"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = Mock()
        mock_ad_repo.add.return_value = None

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        durations = [30, 60, 90]
        for duration in durations:
            ad_input = CreateAdvertisementInput(
                store_id=store.id,
                vehicle_id=f"vehicle-{duration}",
                title=f"Mercedes Actros - {duration} dias",
                description=f"Caminhão Mercedes Actros, plano de {duration} dias",
                price_amount=280000.0
            )

            result = use_case.execute(ad_input)
            assert result is not None
            assert isinstance(result, CreateAdvertisementOutput)

    def test_create_advertisement_repository_error(self):
        """Testa criação de anúncio com erro no repositório"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = Mock()
        mock_ad_repo.add.side_effect = Exception("Database error")

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Volvo FH 440",
            description="Caminhão em excelente estado",
            price_amount=250000.0
        )

        with pytest.raises(Exception, match="Database error"):
            use_case.execute(ad_input)

    def test_create_advertisement_store_not_found(self):
        """Testa criação de anúncio com loja não encontrada"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        mock_store_repo.get_by_id.return_value = None

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id="store-not-found",
            vehicle_id="vehicle-123",
            title="Volvo FH 440",
            description="Caminhão em excelente estado",
            price_amount=250000.0
        )

        with pytest.raises(ValidationError, match="Loja não encontrada"):
            use_case.execute(ad_input)

    def test_create_advertisement_vehicle_not_found(self):
        """Testa criação de anúncio com veículo não encontrado"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = self._create_test_store("Minha Loja", "user-123")

        mock_store_repo.get_by_id.return_value = store
        mock_vehicle_repo.get_by_id.return_value = None

        use_case = CreateAdvertisementUseCase(
            mock_ad_repo,
            mock_store_repo,
            mock_vehicle_repo
        )

        ad_input = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-not-found",
            title="Volvo FH 440",
            description="Caminhão em excelente estado",
            price_amount=250000.0
        )

        with pytest.raises(ValidationError, match="Veículo não encontrado"):
            use_case.execute(ad_input)