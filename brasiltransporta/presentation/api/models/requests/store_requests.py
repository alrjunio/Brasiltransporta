from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

class CreateStoreRequest(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    owner_id: UUID
    cnpj: str | None = None
