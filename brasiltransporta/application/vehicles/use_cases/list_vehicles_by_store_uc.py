import uuid
from typing import List

class ListVehiclesByStoreUseCase:
    def __init__(self, vehicle_repo) -> None:
        self._repo = vehicle_repo

    def execute(self, store_id: uuid.UUID, *, limit: int = 50, offset: int = 0):
        return self._repo.list_by_store(store_id, limit=limit, offset=offset)
