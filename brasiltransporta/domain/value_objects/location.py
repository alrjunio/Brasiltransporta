from dataclasses import dataclass
from brasiltransporta.domain.errors import ValidationError

@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise ValidationError("Latitude deve estar entre -90 e 90 graus.")
        if not (-180 <= self.longitude <= 180):
            raise ValidationError("Longitude deve estar entre -180 e 180 graus.")

    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})"
