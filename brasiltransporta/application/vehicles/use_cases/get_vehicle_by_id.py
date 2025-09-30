import uuid
from typing import Optional

class GetVehicleByIdUseCase:
    def __init__(self, vehicle_repo) -> None:
        self._repo = vehicle_repo

    def execute(self, vehicle_id: uuid.UUID):
        return self._repo.get_by_id(vehicle_id)
