from typing import Optional
from pydantic import BaseModel, EmailStr


class RegisterUserResponse(BaseModel):
    id: str


class UserDetailResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    profession: Optional[str] = None
    region: Optional[str] = None
