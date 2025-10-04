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
    
    
class CreateTransactionResponse(BaseModel):
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str = "BRL"
    payment_method: str
    status: str

class TransactionDetailResponse(BaseModel):
    id: str
    user_id: str
    plan_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    external_payment_id: Optional[str] = None

