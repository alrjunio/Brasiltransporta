import pytest
from unittest.mock import Mock
from brasiltransporta.domain.errors.errors import ValidationError
from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementUseCase, CreateAdvertisementInput
from brasiltransporta.application.advertisements.use_cases.get_advertisement_by_id import GetAdvertisementByIdUseCase, GetAdvertisementByIdInput
from brasiltransporta.application.advertisements.use_cases.publish_advertisement import PublishAdvertisementUseCase, PublishAdvertisementInput
from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.vehicle import Vehicle


class TestCreateAdvertisementUseCase:

    def test_execute_success(self):
        """Testa criação bem-sucedida de anúncio"""
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create(\"Minha Loja\", \"user-123\")
        mock_store_repo.get_by_id.return_value = store

        vehicle = Vehicle.create(\"ABC1234\", \"Volvo\", \"FH 540\", 2022, \"user-123\")
        mock_vehicle_repo.get_by_id.return_value = vehicle

        advertisement = Advertisement.create(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )
        mock_ad_repo.create.return_value = advertisement

        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )

        result = use_case.execute(input_data)

        assert result.advertisement_id == advertisement.id
        mock_ad_repo.create.assert_called_once()

    def test_execute_store_not_found(self):
        \"\"\"Testa criação com loja não encontrada\"\"\"
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        mock_store_repo.get_by_id.return_value = None

        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )

        with pytest.raises(ValidationError, match=\"Loja não encontrada\"):
            use_case.execute(input_data)

    def test_execute_vehicle_not_found(self):
        \"\"\"Testa criação com veículo não encontrado\"\"\"
        mock_ad_repo = Mock()
        mock_store_repo = Mock()
        mock_vehicle_repo = Mock()

        store = Store.create(\"Minha Loja\", \"user-123\")
        mock_store_repo.get_by_id.return_value = store

        mock_vehicle_repo.get_by_id.return_value = None

        use_case = CreateAdvertisementUseCase(mock_ad_repo, mock_store_repo, mock_vehicle_repo)
        input_data = CreateAdvertisementInput(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )

        with pytest.raises(ValidationError, match=\"Veículo não encontrado\"):
            use_case.execute(input_data)


class TestGetAdvertisementByIdUseCase:

    def test_execute_success(self):
        \"\"\"Testa busca bem-sucedida de anúncio\"\"\"
        mock_ad_repo = Mock()
        advertisement = Advertisement.create(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )
        mock_ad_repo.get_by_id.return_value = advertisement

        use_case = GetAdvertisementByIdUseCase(mock_ad_repo)
        input_data = GetAdvertisementByIdInput(advertisement_id=advertisement.id)

                with pytest.raises(ValidationError, match="Veículo não encontrado"):
            use_case.execute(input_data)


        assert result.advertisement == advertisement

    def test_execute_not_found(self):
        \"\"\"Testa busca de anúncio não encontrado\"\"\"
        mock_ad_repo = Mock()
        mock_ad_repo.get_by_id.return_value = None

        use_case = GetAdvertisementByIdUseCase(mock_ad_repo)
        input_data = GetAdvertisementByIdInput(advertisement_id=\"invalid-id\")

        with pytest.raises(ValidationError, match=\"Anúncio não encontrado\"):
            use_case.execute(input_data)


class TestPublishAdvertisementUseCase:

    def test_execute_success(self):
        \"\"\"Testa publicação bem-sucedida de anúncio\"\"\"
        mock_ad_repo = Mock()
        advertisement = Advertisement.create(
            store_id=\"store-123\",
            vehicle_id=\"vehicle-456\",
            title=\"Caminhão Volvo 2022\",
            description=\"Caminhão em excelente estado\",
            price_amount=150000.00
        )
        # Garante que está em draft
        advertisement._status = \"draft\"
        mock_ad_repo.get_by_id.return_value = advertisement
        mock_ad_repo.update = Mock()

        use_case = PublishAdvertisementUseCase(mock_ad_repo)
        input_data = PublishAdvertisementInput(advertisement_id=advertisement.id)

        result = use_case.execute(input_data)

        assert result.success is True
        mock_ad_repo.update.assert_called_once_with(advertisement)

    def test_execute_advertisement_not_found(self):
        \"\"\"Testa publicação de anúncio não encontrado\"\"\"
        mock_ad_repo = Mock()
        mock_ad_repo.get_by_id.return_value = None

        use_case = PublishAdvertisementUseCase(mock_ad_repo)
        input_data = PublishAdvertisementInput(advertisement_id=\"invalid-id\")

        with pytest.raises(ValidationError, match=\"Anúncio não encontrado\"):
            use_case.execute(input_data)
