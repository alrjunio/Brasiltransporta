from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterUserResponse(BaseModel):
    id: UUID


class UserDetailResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    profession: Optional[str] = None
    region: Optional[str] = None
