from pydantic import BaseModel
from datetime import datetime

class VehicleResponse(BaseModel):
    id: str
    store_id: str
    brand: str
    model: str
    year: int
    plate: str
    created_at: datetime
