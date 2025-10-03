from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class VehicleBase(BaseModel):
    brand: str
    model: str
    year: int
    price: float
    mileage: Optional[int] = None
    vehicle_type: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    description: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True