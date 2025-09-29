from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr

from brasiltransporta.presentation.api.models.requests.user_requests import RegisterUserRequest
from brasiltransporta.presentation.api.models.responses.user_responses import (
    RegisterUserResponse,
    UserDetailResponse,
)

from brasiltransporta.application.users.use_cases.register_user import (
    RegisterUserUseCase,
    RegisterUserInput,
)
from brasiltransporta.presentation.api.di.get_register_user_uc import get_register_user_uc

from brasiltransporta.application.users.use_cases.get_user_by_id import GetUserByIdUseCase
from brasiltransporta.presentation.api.di.get_user_by_id_uc import get_user_by_id_uc

from brasiltransporta.application.users.use_cases.get_user_by_email import GetUserByEmailUseCase
from brasiltransporta.presentation.api.di.get_user_by_email_uc import get_user_by_email_uc

router = APIRouter()


@router.post("/users", response_model=RegisterUserResponse, status_code=201)
def register(
    payload: RegisterUserRequest,
    uc: RegisterUserUseCase = Depends(get_register_user_uc),
):
    out = uc.execute(RegisterUserInput(**payload.dict()))
    return RegisterUserResponse(id=out.user_id)


@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user_by_id(
    user_id: str,
    uc: GetUserByIdUseCase = Depends(get_user_by_id_uc),
):
    out = uc.execute(user_id)
    if out is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return UserDetailResponse(**asdict(out))


@router.get("/users", response_model=UserDetailResponse)
def get_user_by_email(
    email: EmailStr = Query(..., description="E-mail do usuário"),
    uc: GetUserByEmailUseCase = Depends(get_user_by_email_uc),
):
    out = uc.execute(str(email))
    if out is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return UserDetailResponse(**asdict(out))
