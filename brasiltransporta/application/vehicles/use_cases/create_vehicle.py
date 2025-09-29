from dataclasses import dataclass
from brasiltransporta.domain.value_objects.vehicle_specs import VehicleSpecs
from brasiltransporta.domain.entities.vehicle import Vehicle
from brasiltransporta.domain.repositories.vehicle_repository import VehicleRepository


@dataclass(frozen=True)
class CreateVehicleInput:
    model: str
    year: int
    capacity_kg: float


@dataclass(frozen=True)
class CreateVehicleOutput:
    vehicle_id: str


class CreateVehicleUseCase:
    def __init__(self, vehicles: VehicleRepository):
        self._vehicles = vehicles

    def execute(self, data: CreateVehicleInput) -> CreateVehicleOutput:
        # 1) construir VO com validação de domínio
        specs = VehicleSpecs(
            model=data.model,
            year=data.year,
            capacity_kg=data.capacity_kg,
        )
        # 2) criar entidade
        vehicle = Vehicle.create(specs=specs)
        # 3) persistir via contrato
        self._vehicles.add(vehicle)
        # 4) retornar DTO de saída
        return CreateVehicleOutput(vehicle_id=vehicle.id)
