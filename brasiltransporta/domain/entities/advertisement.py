from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum

from brasiltransporta.domain.errors import ValidationError


class AdvertisementStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    # adicione outros se precisar (ex.: ARCHIVED = "archived")


@dataclass
class Advertisement:
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    status: AdvertisementStatus = AdvertisementStatus.DRAFT
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
    ) -> "Advertisement":
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            vehicle_id=vehicle_id,
            title=title,
            description=description or "",
            price_amount=float(price_amount),
            status=AdvertisementStatus.DRAFT,
        )

    def publish(self) -> None:
        # mensagem EXATA esperada pelos testes
        if self.status != AdvertisementStatus.DRAFT:
            raise ValidationError("Somente anúncios em 'draft' podem ser publicados.")
        self.status = AdvertisementStatus.PUBLISHED
        self.updated_at = datetime.utcnow()
