from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class GetAdvertisementByIdOutput:
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    price_currency: str
    status: str
    is_featured: bool
    views: int
    created_at: str
    updated_at: str

class GetAdvertisementByIdUseCase:
    def __init__(self, advertisements):
        self._advertisements = advertisements

    def execute(self, advertisement_id: str) -> Optional[GetAdvertisementByIdOutput]:
        advertisement = self._advertisements.get_by_id(advertisement_id)
        if not advertisement:
            return None
        
        return GetAdvertisementByIdOutput(
            id=advertisement.id,
            store_id=advertisement.store_id,
            vehicle_id=advertisement.vehicle_id,
            title=advertisement.title,
            description=advertisement.description,
            price_amount=advertisement.price_amount,
            price_currency=advertisement.price_currency,
            status=advertisement.status.value,
            is_featured=advertisement.is_featured,
            views=advertisement.views,
            created_at=advertisement.created_at.isoformat(),
            updated_at=advertisement.updated_at.isoformat()
        )
