from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    id: str
