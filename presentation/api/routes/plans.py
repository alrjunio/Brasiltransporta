# presentation/api/routes/plans.py
from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

from brasiltransporta.presentation.api.models.requests.plan_requests import CreatePlanRequest
from brasiltransporta.presentation.api.models.responses.plan_responses import (
    CreatePlanResponse,
    PlanDetailResponse,
    ListPlansResponse,
    PlanListItem,
)

from brasiltransporta.application.plans.use_cases.create_plan import (
    CreatePlanUseCase,
    CreatePlanInput,
)
from brasiltransporta.application.plans.use_cases.get_plan_by_id import (
    GetPlanByIdUseCase,
)
from brasiltransporta.application.plans.use_cases.list_active_plans import (
    ListActivePlansUseCase,
)

router = APIRouter(prefix="/plans", tags=["plans"])

@router.post("", response_model=CreatePlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    payload: CreatePlanRequest,
    uc: CreatePlanUseCase = Depends(),  # DI provider necessário
):
    try:
        out = uc.execute(CreatePlanInput(**payload.model_dump()))
        return CreatePlanResponse(id=out.plan_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@router.get("/{plan_id}", response_model=PlanDetailResponse)
def get_plan_by_id(
    plan_id: str,
    uc: GetPlanByIdUseCase = Depends(),  # DI provider necessário
):
    out = uc.execute(plan_id)
    if out is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano não encontrado."
        )
    return PlanDetailResponse(**asdict(out))

@router.get("", response_model=ListPlansResponse)
def list_active_plans(
    uc: ListActivePlansUseCase = Depends(),  # DI provider necessário
):
    out = uc.execute()
    plan_items = [
        PlanListItem(**asdict(plan)) for plan in out.plans
    ]
    return ListPlansResponse(plans=plan_items)
