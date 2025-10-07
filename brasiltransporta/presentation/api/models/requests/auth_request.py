from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    """Schema para requisição de refresh token"""
    refresh_token: str

class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None

class PhoneLoginRequest(BaseModel):
    """Schema para login com celular (para futuro)"""
    phone: str
    code: Optional[str] = None  # Para verificação por código

class PasswordResetRequest(BaseModel):
    """Schema para reset de senha"""
    email: EmailStr
    new_password: str
    reset_token: Optional[str] = None