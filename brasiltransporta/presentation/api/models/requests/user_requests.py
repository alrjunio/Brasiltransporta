from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    phone: str | None = None
    birth_date: str | None = None  # ISO "YYYY-MM-DD" (pode virar date depois)
    profession: str | None = None
    region: str | None = None
