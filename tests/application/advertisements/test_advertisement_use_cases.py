import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta

from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.entities.store import Store
from brasiltransporta.domain.entities.plan import Plan
from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementUseCase


class TestCreateAdvertisementUseCase:
    """Testa casos de uso de anúncios"""
    
    @pytest.mark.asyncio
    async def test_create_advertisement_success(self):
        """Testa criação bem-sucedida de anúncio"""
        # Arrange
        mock_uow = Mock()
        mock_uow.advertisements = AsyncMock()
        mock_uow.commit = AsyncMock()
        
        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create("Plano Básico", 100.0, 30, "Plano básico de anúncio")
        
        use_case = CreateAdvertisementUseCase(mock_uow)
        
        # Act
        result = await use_case.execute(
            title="Anúncio Teste",
            description="Descrição do anúncio",
            price=1500.50,
            store_id=store.id,
            plan_id=plan.id
        )
        
        # Assert
        assert result.is_success()
        assert result.value.title == "Anúncio Teste"
        mock_uow.advertisements.add.assert_called_once()
        mock_uow.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_advertisement_invalid_price(self):
        """Testa criação de anúncio com preço inválido"""
        # Arrange
        mock_uow = Mock()
        mock_uow.advertisements = AsyncMock()
        
        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create("Plano Básico", 100.0, 30, "Plano básico de anúncio")
        
        use_case = CreateAdvertisementUseCase(mock_uow)
        
        # Act
        result = await use_case.execute(
            title="Anúncio Teste",
            description="Descrição do anúncio",
            price=-100.0,  # Preço inválido
            store_id=store.id,
            plan_id=plan.id
        )
        
        # Assert
        assert result.is_failure()
        assert "price" in str(result.error).lower()

    @pytest.mark.asyncio
    async def test_create_advertisement_missing_required_fields(self):
        """Testa criação de anúncio com campos obrigatórios faltando"""
        # Arrange
        mock_uow = Mock()
        mock_uow.advertisements = AsyncMock()
        
        use_case = CreateAdvertisementUseCase(mock_uow)
        
        # Act
        result = await use_case.execute(
            title="",  # Título vazio
            description="Descrição do anúncio",
            price=1500.50,
            store_id="store-123",
            plan_id="plan-123"
        )
        
        # Assert
        assert result.is_failure()

    @pytest.mark.asyncio
    async def test_create_advertisement_with_vehicle_info(self):
        """Testa criação de anúncio com informações de veículo"""
        # Arrange
        mock_uow = Mock()
        mock_uow.advertisements = AsyncMock()
        mock_uow.commit = AsyncMock()
        
        store = Store.create("Loja de Veículos", "user-123")
        plan = Plan.create("Plano Premium", 200.0, 60, "Plano premium de anúncio")
        
        use_case = CreateAdvertisementUseCase(mock_uow)
        
        # Act
        result = await use_case.execute(
            title="Caminhão Mercedes 2023",
            description="Caminhão em excelente estado",
            price=250000.0,
            store_id=store.id,
            plan_id=plan.id,
            vehicle_info={
                "brand": "Mercedes",
                "model": "Actros",
                "year": 2023,
                "mileage": 50000
            }
        )
        
        # Assert
        assert result.is_success()
        advertisement = result.value
        assert advertisement.vehicle_info["brand"] == "Mercedes"
        assert advertisement.vehicle_info["model"] == "Actros"

    @pytest.mark.asyncio
    async def test_create_advertisement_different_plan_durations(self):
        """Testa criação de anúncio com diferentes durações de plano"""
        # Arrange
        mock_uow = Mock()
        mock_uow.advertisements = AsyncMock()
        mock_uow.commit = AsyncMock()
        
        store = Store.create("Minha Loja", "user-123")
        
        # Testar diferentes planos
        plans = [
            Plan.create("Plano 7 Dias", 50.0, 7, "Plano semanal"),
            Plan.create("Plano 30 Dias", 100.0, 30, "Plano mensal"),
            Plan.create("Plano 90 Dias", 250.0, 90, "Plano trimestral")
        ]
        
        use_case = CreateAdvertisementUseCase(mock_uow)
        
        for plan in plans:
            # Act
            result = await use_case.execute(
                title=f"Anúncio com {plan.duration_days} dias",
                description="Descrição do anúncio",
                price=1000.0,
                store_id=store.id,
                plan_id=plan.id
            )
            
            # Assert
            assert result.is_success()
            advertisement = result.value
            expected_expiry = datetime.now() + timedelta(days=plan.duration_days)
            # Verifica se a data de expiração está próxima do esperado (com margem de 1 minuto)
            time_diff = abs((advertisement.expires_at - expected_expiry).total_seconds())
            assert time_diff < 60  # Menos de 1 minuto de diferença

    @pytest.mark.asyncio
    async def test_create_advertisement_repository_error(self):
        """Testa criação de anúncio quando o repositório falha"""
        # Arrange
        mock_uow = Mock()
        mock_uow.advertisements = AsyncMock()
        mock_uow.advertisements.add.side_effect = Exception("Database error")
        mock_uow.rollback = AsyncMock()
        
        store = Store.create("Minha Loja", "user-123")
        plan = Plan.create("Plano Básico", 100.0, 30, "Plano básico de anúncio")
        
        use_case = CreateAdvertisementUseCase(mock_uow)
        
        # Act
        result = await use_case.execute(
            title="Anúncio Teste",
            description="Descrição do anúncio",
            price=1500.50,
            store_id=store.id,
            plan_id=plan.id
        )
        
        # Assert
        assert result.is_failure()
        assert "database" in str(result.error).lower()
        mock_uow.rollback.assert_called_once()