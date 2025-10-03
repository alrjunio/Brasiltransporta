from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from brasiltransporta.application.advertisements.use_cases.create_advertisement import (
    CreateAdvertisementUseCase, CreateAdvertisementInput
)
from brasiltransporta.application.advertisements.use_cases.publish_advertisement import (
    PublishAdvertisementUseCase, PublishAdvertisementInput
)

# Estas funções são intencionalmente simples: nos testes elas serão "patchadas".
def get_create_advertisement_uc() -> CreateAdvertisementUseCase:
    raise RuntimeError("DI não configurado (esperado ser patchado nos testes)")

def get_get_advertisement_by_id_uc():
    raise RuntimeError("DI não configurado (esperado ser patchado nos testes)")

router = APIRouter(prefix="/advertisements", tags=["advertisements"])

class CreateAdvertisementRequest(BaseModel):
    store_id: str
    vehicle_id: str
    title: str
    description: Optional[str] = ""
    price_amount: float

class CreateAdvertisementResponse(BaseModel):
    id: str

@router.post("", response_model=CreateAdvertisementResponse, status_code=status.HTTP_201_CREATED)
def create_advertisement(
    payload: CreateAdvertisementRequest,
    uc: CreateAdvertisementUseCase = Depends(get_create_advertisement_uc),
):
    out = uc.execute(CreateAdvertisementInput(**payload.model_dump()))
    return {"id": out.advertisement_id}

class AdvertisementDetailResponse(BaseModel):
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    status: str

@router.get("/{advertisement_id}", response_model=AdvertisementDetailResponse)
def get_advertisement(advertisement_id: str, uc = Depends(get_get_advertisement_by_id_uc)):
    out = uc.execute(advertisement_id)
    if out is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    # Nos testes, 'out' é um Mock com atributos; FastAPI/Pydantic serializam.
    return out
