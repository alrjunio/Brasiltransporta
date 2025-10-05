import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta

from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.plan import Plan, PlanType, BillingCycle
from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementUseCase
from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementInput


class TestCreateAdvertisementUseCase:
    """Testa casos de uso de anúncios"""

    def test_create_advertisement_success(self):
        """Testa criação bem-sucedida de anúncio"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create(
            name="Plano Básico",
            description="Plano básico de anúncio",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=100.0
        )

        mock_store_repo.get_by_id.return_value = store

        use_case = CreateAdvertisementUseCase(
            ad_repo=mock_ad_repo,
            store_repo=mock_store_repo,
            vehicle_repo=mock_vehicle_repo
        )

        # Act
        input_data = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Anúncio Teste",
            description="Descrição do anúncio",
            price_amount=1500.50
        )
        result = use_case.execute(input_data)

        # Assert
        assert result.advertisement_id is not None
        assert len(result.advertisement_id) > 0
        mock_ad_repo.add.assert_called_once()

    def test_create_advertisement_invalid_price(self):
        """Testa criação de anúncio com preço inválido"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create(
            name="Plano Básico",
            description="Plano básico de anúncio",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=100.0
        )

        mock_store_repo.get_by_id.return_value = store

        use_case = CreateAdvertisementUseCase(
            ad_repo=mock_ad_repo,
            store_repo=mock_store_repo,
            vehicle_repo=mock_vehicle_repo
        )

        # Act & Assert
        input_data = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Anúncio Teste",
            description="Descrição do anúncio",
            price_amount=-100.0  # Preço inválido
        )
        
        with pytest.raises(Exception) as exc_info:
            use_case.execute(input_data)
        
        assert "preço" in str(exc_info.value).lower()

    def test_create_advertisement_missing_required_fields(self):
        """Testa criação de anúncio com campos obrigatórios faltando"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create("Minha Loja", "user-123")
        mock_store_repo.get_by_id.return_value = store

        use_case = CreateAdvertisementUseCase(
            ad_repo=mock_ad_repo,
            store_repo=mock_store_repo,
            vehicle_repo=mock_vehicle_repo
        )

        # Act & Assert - Testar sem título
        input_data = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="",  # Título vazio
            description="Descrição do anúncio",
            price_amount=1500.50
        )
        
        with pytest.raises(Exception) as exc_info:
            use_case.execute(input_data)
        
        assert "título" in str(exc_info.value).lower()

    def test_create_advertisement_with_vehicle_info(self):
        """Testa criação de anúncio com informações do veículo"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create(
            name="Plano Premium",
            description="Plano premium de anúncio",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=200.0
        )

        mock_store_repo.get_by_id.return_value = store

        use_case = CreateAdvertisementUseCase(
            ad_repo=mock_ad_repo,
            store_repo=mock_store_repo,
            vehicle_repo=mock_vehicle_repo
        )

        # Act
        input_data = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-456",
            title="Carro Esportivo",
            description="Carro em ótimo estado",
            price_amount=50000.0
        )
        result = use_case.execute(input_data)

        # Assert
        assert result.advertisement_id is not None
        mock_ad_repo.add.assert_called_once()

    def test_create_advertisement_different_plan_durations(self):
        """Testa criação de anúncio com diferentes durações de plano"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create("Minha Loja", "user-123")
        mock_store_repo.get_by_id.return_value = store

        use_case = CreateAdvertisementUseCase(
            ad_repo=mock_ad_repo,
            store_repo=mock_store_repo,
            vehicle_repo=mock_vehicle_repo
        )

        # Act
        input_data = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-789",
            title="Moto Custom",
            description="Moto personalizada",
            price_amount=25000.0
        )
        result = use_case.execute(input_data)

        # Assert
        assert result.advertisement_id is not None
        mock_ad_repo.add.assert_called_once()

    def test_create_advertisement_repository_error(self):
        """Testa criação de anúncio com erro no repositório"""
        # Arrange
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create(
            name="Plano Básico",
            description="Plano básico de anúncio",
            plan_type=PlanType.PREMIUM,
            billing_cycle=BillingCycle.MONTHLY,
            price_amount=100.0
        )

        mock_store_repo.get_by_id.return_value = store
        # Simular erro no repositório
        mock_ad_repo.add.side_effect = Exception("Erro no banco de dados")

        use_case = CreateAdvertisementUseCase(
            ad_repo=mock_ad_repo,
            store_repo=mock_store_repo,
            vehicle_repo=mock_vehicle_repo
        )

        # Act & Assert
        input_data = CreateAdvertisementInput(
            store_id=store.id,
            vehicle_id="vehicle-123",
            title="Anúncio Teste",
            description="Descrição do anúncio",
            price_amount=1500.50
        )
        
        with pytest.raises(Exception) as exc_info:
            use_case.execute(input_data)
        
        assert "erro" in str(exc_info.value).lower()
