from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from brasiltransporta.application.advertisements.use_cases.create_advertisement import CreateAdvertisementInput, CreateAdvertisementOutput
from brasiltransporta.application.advertisements.use_cases.get_advertisement_by_id import GetAdvertisementByIdOutput
from brasiltransporta.presentation.api.models.requests.advertisement_requests import CreateAdvertisementRequest
from brasiltransporta.presentation.api.models.responses.advertisement_responses import (
    PublishAdvertisementResponse,
    AdvertisementDetailResponse,
    CreateAdvertisementResponse,
)
from brasiltransporta.presentation.api.models.requests.advertisement_requests import (
    CreateAdvertisementRequest,
)

from brasiltransporta.presentation.api.models.requests.advertisement_requests import (
    CreateAdvertisementRequest,
)

from brasiltransporta.application.advertisements.use_cases.publish_advertisement import PublishAdvertisementInput, PublishAdvertisementUseCase

# Importe as dependências do di
from brasiltransporta.presentation.api.di.dependencies import (
    get_create_advertisement_uc, 
    get_get_advertisement_by_id_uc, 
    get_publish_advertisement_uc
)

router = APIRouter(prefix="/advertisements", tags=["advertisements"])

@router.post("/", response_model=CreateAdvertisementOutput, status_code=201)
async def create_advertisement(
    request: CreateAdvertisementRequest,
    use_case = Depends(get_create_advertisement_uc)
):
    try:
        input_data = CreateAdvertisementInput(
            store_id=request.store_id,
            vehicle_id=request.vehicle_id,
            title=request.title,
            description=request.description,
            price_amount=request.price_amount,
        )
        result = use_case.execute(input_data)
        return CreateAdvertisementOutput(advertisement_id=result.advertisement_id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/{advertisement_id}", response_model=GetAdvertisementByIdOutput)
async def get_advertisement(
    advertisement_id: str,
    use_case = Depends(get_get_advertisement_by_id_uc)
):
    result = use_case.execute(advertisement_id)
    if not result:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return result

@router.post("/{advertisement_id}/publish", response_model=PublishAdvertisementResponse)
def publish_advertisement(
    advertisement_id: str,
    use_case: PublishAdvertisementUseCase = Depends(),
):
    input_data = PublishAdvertisementInput(advertisement_id=advertisement_id)
    result = use_case.execute(input_data)
    return PublishAdvertisementResponse(**result.dict())