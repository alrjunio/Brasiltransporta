from fastapi import APIRouter, Depends, status

from brasiltransporta.presentation.api.models.requests.user_requests import RegisterUserRequest
from brasiltransporta.presentation.api.models.responses.user_responses import RegisterUserResponse
from brasiltransporta.application.users.use_cases.register_user import (
    RegisterUserUseCase,
    RegisterUserInput,
)
from brasiltransporta.presentation.api.di.get_register_user_uc import get_register_user_uc


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=RegisterUserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: RegisterUserRequest,
    uc: RegisterUserUseCase = Depends(get_register_user_uc),
) -> RegisterUserResponse:
    out = uc.execute(RegisterUserInput(**payload.model_dump()))
    return RegisterUserResponse(id=out.user_id)
