# domain/entities/advertisement.py
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum
from brasiltransporta.domain.errors import ValidationError
from brasiltransporta.domain.value_objects.money import Money

class AdvertisementStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    SOLD = "sold"
    EXPIRED = "expired"

@dataclass
class Advertisement:
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price: Money
    status: AdvertisementStatus
    is_featured: bool
    views: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        store_id: str,
        vehicle_id: str,
        title: str,
        description: str,
        price_amount: float,
        price_currency: str = "BRL"
    ) -> "Advertisement":
        if not title or len(title.strip()) < 5:
            raise ValidationError("Título deve ter pelo menos 5 caracteres.")
        if not description or len(description.strip()) < 10:
            raise ValidationError("Descrição deve ter pelo menos 10 caracteres.")
        if price_amount <= 0:
            raise ValidationError("Preço deve ser maior que zero.")

        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            vehicle_id=vehicle_id,
            title=title.strip(),
            description=description.strip(),
            price=Money(amount=price_amount, currency=price_currency),
            status=AdvertisementStatus.DRAFT,
            is_featured=False,
            views=0,
            created_at=now,
            updated_at=now
        )

    def publish(self) -> None:
        if self.status != AdvertisementStatus.DRAFT:
            raise ValidationError("Apenas anúncios em rascunho podem ser publicados.")
        self.status = AdvertisementStatus.ACTIVE
        self.updated_at = datetime.utcnow()

    def mark_as_sold(self) -> None:
        self.status = AdvertisementStatus.SOLD
        self.updated_at = datetime.utcnow()

    def increment_views(self) -> None:
        self.views += 1
        self.updated_at = datetime.utcnow()
