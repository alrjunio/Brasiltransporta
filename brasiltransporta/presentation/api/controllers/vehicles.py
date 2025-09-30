import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime  

from brasiltransporta.application.vehicles.use_cases.create_vehicle import CreateVehicleInput
from brasiltransporta.presentation.api.di.get_create_vehicle_uc import get_create_vehicle_uc
from brasiltransporta.presentation.api.di.get_vehicle_by_id_uc import get_vehicle_by_id_uc
from brasiltransporta.presentation.api.di.list_vehicles_by_store_uc import get_list_vehicles_by_store_uc

from brasiltransporta.presentation.api.models.requests.vehicle_requests import CreateVehicleRequest
from brasiltransporta.presentation.api.models.responses.vehicle_responses import VehicleResponse
from brasiltransporta.domain.errors import ValidationError

router = APIRouter(tags=["vehicles"])

@router.post("/stores/{store_id}/vehicles", status_code=status.HTTP_201_CREATED)
def create_vehicle(
    store_id: uuid.UUID,
    payload: CreateVehicleRequest,
    uc = Depends(get_create_vehicle_uc),
):
    try:
        new_id = uc.execute(
            CreateVehicleInput(
                store_id=store_id,
                brand=payload.brand,
                model=payload.model,
                year=payload.year,
                plate=payload.plate,
            )
        )
        return {"id": str(new_id)}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(
    vehicle_id: uuid.UUID,
    uc = Depends(get_vehicle_by_id_uc),
):
    v = uc.execute(vehicle_id)
    if not v:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    return VehicleResponse(
        id=str(v.id),
        store_id=str(v.store_id),
        brand=v.brand,
        model=v.model,
        year=v.year,
        plate=v.plate,
        created_at=datetime.now(),  
    )

@router.get("/stores/{store_id}/vehicles", response_model=list[VehicleResponse])
def list_vehicles_by_store(
    store_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    uc = Depends(get_list_vehicles_by_store_uc),
):
    rows = uc.execute(store_id, limit=limit, offset=offset)
    return [
        VehicleResponse(
            id=str(v.id),
            store_id=str(v.store_id),
            brand=v.brand,
            model=v.model,
            year=v.year,
            plate=v.plate,
            created_at=datetime.now(),
        )
        for v in rows
    ]