# presentation/api/routes/advertisements.py
from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

from brasiltransporta.presentation.api.models.requests.advertisement_requests import (
    CreateAdvertisementRequest,
    PublishAdvertisementRequest,
)
from brasiltransporta.presentation.api.models.responses.advertisement_responses import (
    CreateAdvertisementResponse,
    AdvertisementDetailResponse,
    PublishAdvertisementResponse,
)

from brasiltransporta.application.advertisements.use_cases.create_advertisement import (
    CreateAdvertisementUseCase,
    CreateAdvertisementInput,
)
from brasiltransporta.application.advertisements.use_cases.get_advertisement_by_id import (
    GetAdvertisementByIdUseCase,
)
from brasiltransporta.application.advertisements.use_cases.publish_advertisement import (
    PublishAdvertisementUseCase,
    PublishAdvertisementInput,
)

router = APIRouter(prefix="/advertisements", tags=["advertisements"])

@router.post("", response_model=CreateAdvertisementResponse, status_code=status.HTTP_201_CREATED)
def create_advertisement(
    payload: CreateAdvertisementRequest,
    uc: CreateAdvertisementUseCase = Depends(),  # DI provider necessário
):
    try:
        out = uc.execute(CreateAdvertisementInput(**payload.model_dump()))
        return CreateAdvertisementResponse(id=out.advertisement_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@router.get("/{advertisement_id}", response_model=AdvertisementDetailResponse)
def get_advertisement_by_id(
    advertisement_id: str,
    uc: GetAdvertisementByIdUseCase = Depends(),  # DI provider necessário
):
    out = uc.execute(advertisement_id)
    if out is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anúncio não encontrado."
        )
    return AdvertisementDetailResponse(**asdict(out))

@router.post("/{advertisement_id}/publish", response_model=PublishAdvertisementResponse)
def publish_advertisement(
    advertisement_id: str,
    uc: PublishAdvertisementUseCase = Depends(),  # DI provider necessário
):
    try:
        out = uc.execute(PublishAdvertisementInput(advertisement_id=advertisement_id))
        return PublishAdvertisementResponse(success=out.success)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
