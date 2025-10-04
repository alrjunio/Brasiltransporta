import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Numeric, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from .base import Base


class AdvertisementModel(Base):
    __tablename__ = "advertisements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price_amount = Column(Numeric(12, 2), nullable=False)
    price_currency = Column(String(3), nullable=False, default="BRL")
    status = Column(String(20), nullable=False, default="draft")
    is_featured = Column(Boolean, nullable=False, default=False)
    views = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_domain(self):
        """
        Converte o AdvertisementModel para uma entidade Advertisement do domínio.
        """
        # Importação local para evitar circularidade
        from brasiltransporta.domain.entities.advertisement import Advertisement, AdvertisementStatus
        
        return Advertisement(
            id=str(self.id),
            store_id=str(self.store_id),
            vehicle_id=str(self.vehicle_id),
            title=self.title,
            description=self.description,
            price_amount=float(self.price_amount),
            price_currency=self.price_currency,
            status=AdvertisementStatus(self.status),
            is_featured=self.is_featured,
            views=self.views,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, advertisement):
        """
        Cria um AdvertisementModel a partir de uma entidade Advertisement do domínio.
        """
        return cls(
            id=uuid.UUID(advertisement.id),
            store_id=uuid.UUID(advertisement.store_id),
            vehicle_id=uuid.UUID(advertisement.vehicle_id),
            title=advertisement.title,
            description=advertisement.description,
            price_amount=advertisement.price_amount,
            price_currency=advertisement.price_currency,
            status=advertisement.status.value,
            is_featured=advertisement.is_featured,
            views=advertisement.views,
            created_at=advertisement.created_at,
            updated_at=advertisement.updated_at or datetime.utcnow()
        )