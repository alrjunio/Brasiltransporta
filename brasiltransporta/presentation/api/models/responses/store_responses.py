from pydantic import BaseModel
from uuid import UUID

class StoreResponse(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
    cnpj: str | None = None
