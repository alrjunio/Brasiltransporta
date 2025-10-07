from pydantic import BaseModel, Field

class SendPhoneCodeRequest(BaseModel):
    phone: str = Field(..., description="Número de telefone com DDD")

class VerifyPhoneCodeRequest(BaseModel):
    phone: str = Field(..., description="Número de telefone com DDD") 
    code: str = Field(..., min_length=6, max_length=6, description="Código de 6 dígitos")

class PhoneLoginRequest(BaseModel):
    phone: str
    code: str