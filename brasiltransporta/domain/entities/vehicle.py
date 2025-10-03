# domain/entities/vehicle.py
from dataclasses import dataclass
from uuid import uuid4

@dataclass
class Vehicle:
    id: str
    store_id: str
    brand: str
    model: str
    year: int
    plate: str

    @classmethod
    def create(cls, store_id: str, brand: str, model: str, year: int, plate: str) -> "Vehicle":
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            brand=brand.strip(),
            model=model.strip(),
            year=year,
            plate=plate.upper().strip()
        )