from dataclasses import dataclass
from uuid import uuid4
from brasiltransporta.domain.value_objects.vehicle_specs import VehicleSpecs

@dataclass
class Vehicle:
    id: str
    specs: VehicleSpecs

    @classmethod
    def create(cls, specs: VehicleSpecs) -> "Vehicle":
        return cls(id=str(uuid4()), specs=specs)