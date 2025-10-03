# presentation/api/models/responses/advertisement_responses.py
from pydantic import BaseModel

class CreateAdvertisementResponse(BaseModel):
    id: str

class AdvertisementDetailResponse(BaseModel):
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

class PublishAdvertisementResponse(BaseModel):
    success: bool
