import pytest
from brasiltransporta.domain.entities.advertisement import Advertisement, AdvertisementStatus

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
        assert advertisement.price_amount == 150000.00
        assert advertisement.status == AdvertisementStatus.DRAFT
        assert advertisement.views == 0
        assert advertisement.is_featured == False

    def test_create_advertisement_invalid_title(self):
        """Testa criação com título inválido"""
        with pytest.raises(ValueError, match="Título deve ter pelo menos 5 caracteres"):
            Advertisement.create(
                store_id="store-123",
                vehicle_id="vehicle-456",
                title="Ab",
                description="Descrição válida",
                price_amount=150000.00
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
