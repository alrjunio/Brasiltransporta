from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Address:
    """Value Object para endereços - imutável"""
    street: str
    city: str
    state: str
    zip_code: str
    coordinates: Optional[Tuple[float, float]] = None  # (latitude, longitude)

    def __post_init__(self):
        """Validações básicas"""
        if not self.street.strip():
            raise ValueError("Street cannot be empty")
        if not self.city.strip():
            raise ValueError("City cannot be empty")
        if not self.state.strip():
            raise ValueError("State cannot be empty")
        if not self.zip_code.strip():
            raise ValueError("Zip code cannot be empty")

    @classmethod
    def create(cls, street: str, city: str, state: str, zip_code: str, 
               lat: Optional[float] = None, lng: Optional[float] = None) -> "Address":
        """Factory method para criar Address"""
        coordinates = (lat, lng) if lat is not None and lng is not None else None
        return cls(
            street=street.strip(),
            city=city.strip(),
            state=state.strip(),
            zip_code=zip_code.strip(),
            coordinates=coordinates
        )