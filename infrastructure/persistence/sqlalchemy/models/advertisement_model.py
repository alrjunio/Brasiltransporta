# infrastructure/persistence/sqlalchemy/models/advertisement_model.py
from __future__ import annotations
from uuid import uuid4
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
from brasiltransporta.domain.entities.advertisement import Advertisement, AdvertisementStatus
from brasiltransporta.domain.value_objects.money import Money

class AdvertisementModel(Base):
    __tablename__ = "advertisements"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    store_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False)
    vehicle_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price_amount: Mapped[float] = mapped_column(nullable=False)
    price_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="BRL")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=AdvertisementStatus.DRAFT.value)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    store = relationship("StoreModel", back_populates="advertisements")
    vehicle = relationship("VehicleModel", back_populates="advertisement")

    @classmethod
    def from_domain(cls, advertisement: Advertisement) -> "AdvertisementModel":
        return cls(
            id=advertisement.id,
            store_id=advertisement.store_id,
            vehicle_id=advertisement.vehicle_id,
            title=advertisement.title,
            description=advertisement.description,
            price_amount=advertisement.price.amount,
            price_currency=advertisement.price.currency,
            status=advertisement.status.value,
            is_featured=advertisement.is_featured,
            views=advertisement.views,
            created_at=advertisement.created_at,
            updated_at=advertisement.updated_at
        )

    def to_domain(self) -> Advertisement:
        return Advertisement(
            id=self.id,
            store_id=self.store_id,
            vehicle_id=self.vehicle_id,
            title=self.title,
            description=self.description,
            price=Money(amount=self.price_amount, currency=self.price_currency),
            status=AdvertisementStatus(self.status),
            is_featured=self.is_featured,
            views=self.views,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
