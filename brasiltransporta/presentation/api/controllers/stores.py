import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from brasiltransporta.presentation.api.models.requests.store_requests import CreateStoreRequest
from brasiltransporta.presentation.api.models.responses.store_responses import StoreResponse
from brasiltransporta.presentation.api.di.get_create_store_uc import get_create_store_uc
from brasiltransporta.presentation.api.di.get_store_by_id_uc import get_store_by_id_uc
from brasiltransporta.application.stores.use_cases.create_store import CreateStoreInput
from brasiltransporta.domain.errors.errors import ValidationError
from brasiltransporta.presentation.api.dependencies.authz import require_roles

router = APIRouter(prefix="/stores", tags=["stores"])

@router.post("", status_code=status.HTTP_201_CREATED, 
        response_model=StoreResponse, 
        dependencies=[Depends(require_roles("seller", "admin"))],
        )
def create_store(
    payload: CreateStoreRequest,
    uc = Depends(get_create_store_uc),
    
):
    try:
        out = uc.execute(CreateStoreInput(
            name=payload.name,
            owner_id=payload.owner_id,
            cnpj=payload.cnpj,
        ))
        return StoreResponse(
            id=out.store_id,
            name=payload.name,
            owner_id=payload.owner_id,
            cnpj=payload.cnpj,
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/{store_id}", 
        response_model=StoreResponse,
        dependencies=[Depends(require_roles("seller", "admin"))],
        )
async def get_store_by_id(
    store_id: uuid.UUID,
    uc = Depends(get_store_by_id_uc),
):
    try:
        s = await uc.execute(store_id)
        return StoreResponse(
            id=s.id,
            name=s.name,
            owner_id=s.owner_id,
            cnpj=getattr(s, "cnpj", None),
        )
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

