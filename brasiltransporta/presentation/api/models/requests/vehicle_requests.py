from pydantic import BaseModel, Field

class CreateVehicleRequest(BaseModel):
    brand: str = Field(..., min_length=1, max_length=80)
    model: str = Field(..., min_length=1, max_length=120)
    year: int
    plate: str = Field(..., min_length=5, max_length=10)
