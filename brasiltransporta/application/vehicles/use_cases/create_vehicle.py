# application/vehicles/use_cases/create_vehicle.py
from dataclasses import dataclass
from datetime import datetime
import re
from uuid import UUID

from brasiltransporta.domain.entities.vehicle import Vehicle
from brasiltransporta.domain.errors.errors import ValidationError

PLATE_RE = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")  # Formato Mercosul

@dataclass
class CreateVehicleInput:
    store_id: UUID
    brand: str
    model: str
    year: int
    plate: str

@dataclass
class CreateVehicleOutput:
    vehicle_id: str

class CreateVehicleUseCase:
    def __init__(self, vehicle_repo) -> None:
        self._repo = vehicle_repo

    async def execute(self, data: CreateVehicleInput) -> CreateVehicleOutput:
        # Validações
        current_year = datetime.now().year
        if not (1950 <= data.year <= current_year + 1):
            raise ValidationError("Ano do veículo inválido.")

        plate = data.plate.upper().strip()
        if not PLATE_RE.match(plate):
            raise ValidationError("Placa inválida. Use formato Mercosul: ABC1D23")

        # Verificar se placa já existe
        existing_vehicle = await self._repo.get_by_plate(plate)
        if existing_vehicle:
            raise ValidationError(f"Já existe um veículo com a placa {plate}")

        # Criar veículo 
        vehicle = Vehicle.create(
            store_id=str(data.store_id),
            brand=data.brand,
            model=data.model,
            year=data.year,
            plate=plate
        )

        # Persistir
        await self._repo.add(vehicle)
    
        return CreateVehicleOutput(vehicle_id=vehicle.id)