# tests/domain/entities/test_advertisement.py
import pytest
from datetime import datetime
from brasiltransporta.domain.entities.advertisement import Advertisement, AdvertisementStatus
from brasiltransporta.domain.errors import ValidationError

class TestAdvertisement:
    def test_create_advertisement_success(self):
        """Testa criação bem-sucedida de anúncio"""
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado, revisado",
            price_amount=150000.00
        )
        
        assert advertisement.id is not None
        assert advertisement.store_id == "store-123"
        assert advertisement.vehicle_id == "vehicle-456"
        assert advertisement.title == "Caminhão Volvo 2022"
        assert advertisement.price.amount == 150000.00
        assert advertisement.status == AdvertisementStatus.DRAFT
        assert advertisement.views == 0
        assert advertisement.is_featured == False

    def test_create_advertisement_invalid_title(self):
        """Testa criação com título inválido"""
        with pytest.raises(ValidationError, match="Título deve ter pelo menos 5 caracteres"):
            Advertisement.create(
                store_id="store-123",
                vehicle_id="vehicle-456",
                title="Ab",
                description="Descrição válida",
                price_amount=150000.00
            )

    def test_create_advertisement_invalid_description(self):
        """Testa criação com descrição inválida"""
        with pytest.raises(ValidationError, match="Descrição deve ter pelo menos 10 caracteres"):
            Advertisement.create(
                store_id="store-123",
                vehicle_id="vehicle-456",
                title="Título válido",
                description="Curta",
                price_amount=150000.00
            )

    def test_create_advertisement_invalid_price(self):
        """Testa criação com preço inválido"""
        with pytest.raises(ValidationError, match="Preço deve ser maior que zero"):
            Advertisement.create(
                store_id="store-123",
                vehicle_id="vehicle-456",
                title="Título válido",
                description="Descrição válida com mais de 10 caracteres",
                price_amount=0
            )

    def test_publish_advertisement_success(self):
        """Testa publicação bem-sucedida de anúncio"""
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        advertisement.publish()
        
        assert advertisement.status == AdvertisementStatus.ACTIVE

    def test_publish_already_published_advertisement(self):
        """Testa publicação de anúncio já publicado"""
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        advertisement.publish()
        
        with pytest.raises(ValidationError, match="Apenas anúncios em rascunho podem ser publicados"):
            advertisement.publish()

    def test_mark_as_sold(self):
        """Testa marcação de anúncio como vendido"""
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        advertisement.mark_as_sold()
        
        assert advertisement.status == AdvertisementStatus.SOLD

    def test_increment_views(self):
        """Testa incremento de visualizações"""
        advertisement = Advertisement.create(
            store_id="store-123",
            vehicle_id="vehicle-456",
            title="Caminhão Volvo 2022",
            description="Caminhão em excelente estado",
            price_amount=150000.00
        )
        
        initial_views = advertisement.views
        advertisement.increment_views()
        
        assert advertisement.views == initial_views + 1
