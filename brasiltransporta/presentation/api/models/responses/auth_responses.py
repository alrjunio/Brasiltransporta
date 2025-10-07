from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class Token(BaseModel):
    """Schema para resposta de tokens JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """Schema para resposta de dados do usuário"""
    id: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class LoginResponse(BaseModel):
    """Schema para resposta de login"""
    user: UserResponse
    tokens: Token

class RefreshResponse(BaseModel):
    """Schema para resposta de refresh token"""
    tokens: Token

class LogoutResponse(BaseModel):
    """Schema para resposta de logout"""
    message: str = "Successfully logged out"

class SessionInfo(BaseModel):
    """Schema para informações de sessão"""
    token_family: str
    created_at: str
    used: bool
    used_at: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None

class SessionsResponse(BaseModel):
    """Schema para resposta de sessões ativas"""
    sessions: List[SessionInfo]

class MessageResponse(BaseModel):
    """Schema genérico para respostas de mensagem"""
    message: str
    detail: Optional[str] = None

class ErrorResponse(BaseModel):
    """Schema para respostas de erro"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None