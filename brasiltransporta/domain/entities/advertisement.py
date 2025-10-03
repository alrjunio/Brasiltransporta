from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional
from brasiltransporta.domain.errors import ValidationError

@dataclass
class Advertisement:
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, store_id: str, vehicle_id: str, title: str, description: str, price_amount: float) -> "Advertisement":
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            vehicle_id=vehicle_id,
            title=title,
            description=description or "",
            price_amount=float(price_amount),
            status="draft",
        )

    def publish(self) -> None:
        if self.status != "draft":
            raise ValidationError("Somente anúncios em 'draft' podem ser publicados.")
        self.status = "published"
        self.updated_at = datetime.utcnow()
