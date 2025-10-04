from dataclasses import dataclass
from brasiltransporta.domain.errors.errors import ValidationError

@dataclass(frozen=True)
class VehicleSpecs:
    model: str
    year: int
    capacity_kg: float

    def __post_init__(self):
        if not self.model or len(self.model) < 2:
            raise ValidationError("Modelo do veículo inválido.")
        if self.year < 1900 or self.year > 2100:
            raise ValidationError("Ano do veículo inválido.")
        if self.capacity_kg <= 0:
            raise ValidationError("Capacidade deve ser maior que zero.")

    def __str__(self) -> str:
        return f"{self.model} ({self.year}) - {self.capacity_kg}kg"