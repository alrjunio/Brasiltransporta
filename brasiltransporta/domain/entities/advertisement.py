from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum

from brasiltransporta.domain.errors import ValidationError


class AdvertisementStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"


@dataclass
class Advertisement:
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    price_currency: str = "BRL"
    status: AdvertisementStatus = AdvertisementStatus.DRAFT
    is_featured: bool = False
    views: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        store_id: str,
        vehicle_id: str,
        title: str,
        description: Optional[str] = "",
        price_amount: float = 0.0,
        price_currency: str = "BRL"
    ) -> "Advertisement":
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            vehicle_id=vehicle_id,
            title=title,
            description=description or "",
            price_amount=float(price_amount),
            price_currency=price_currency,
            status=AdvertisementStatus.DRAFT,
            is_featured=False,
            views=0
        )

    def publish(self) -> None:
        # mensagem EXATA esperada pelos testes
        if self.status != AdvertisementStatus.DRAFT:
            raise ValidationError("Somente anúncios em 'draft' podem ser publicados.")
        self.status = AdvertisementStatus.PUBLISHED
        self.updated_at = datetime.utcnow()


# Exportação explícita para resolver problemas de importação
__all__ = ['Advertisement', 'AdvertisementStatus']