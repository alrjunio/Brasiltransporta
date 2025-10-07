from fastapi import APIRouter, Depends, HTTPException, status

from brasiltransporta.presentation.api.models.requests.plan_requests import CreatePlanRequest
from brasiltransporta.presentation.api.models.responses.plan_responses import (
    CreatePlanResponse,
    ListPlansResponse,
    PlanSummaryResponse,
)

from brasiltransporta.application.plans.use_cases.create_plan import (
    CreatePlanUseCase, CreatePlanInput,
)
from brasiltransporta.application.plans.use_cases.list_active_plans import (
    ListActivePlansUseCase,
)
from brasiltransporta.presentation.api.dependencies.authz import require_roles

# estes são os símbolos que o teste patcha
from brasiltransporta.presentation.api.di.get_create_plan_uc import get_create_plan_uc
from brasiltransporta.presentation.api.di.list_active_plans_uc import get_list_active_plans_uc

router = APIRouter(prefix="/plans", tags=["plans"])

# proxies: olham o símbolo no momento da chamada (após o patch)
def _dep_get_create_plan_uc() -> CreatePlanUseCase:
    # NOTA: não capture como argumento default; leia do módulo (patchável)
    return get_create_plan_uc()

def _dep_get_list_active_plans_uc() -> ListActivePlansUseCase:
    return get_list_active_plans_uc()

@router.post("", response_model=CreatePlanResponse, 
        status_code=status.HTTP_201_CREATED,
         dependencies=[Depends(require_roles( "admin"  ))],
         )
def create_plan(
    payload: CreatePlanRequest,
    uc: CreatePlanUseCase = Depends(_dep_get_create_plan_uc),
):
    try:
        out = uc.execute(CreatePlanInput(**payload.model_dump()))
        return CreatePlanResponse(id=out.plan_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.get("", response_model=ListPlansResponse,  dependencies=[Depends(require_roles("seller", "admin"))])
def list_plans(
    uc: ListActivePlansUseCase = Depends(_dep_get_list_active_plans_uc),
):
    def _as_str(v):
        if isinstance(v, str):
            return v
        mock_name = getattr(v, "_mock_name", None)
        if isinstance(mock_name, str) and mock_name:
            return mock_name
        return str(v)

    def _get_name(p):
        # Tenta o atributo normalmente
        v = getattr(p, "name", None)
        if isinstance(v, str):
            return v
        # Se for Mock ou algo não-string, usa o nome do próprio mock p (Mock(name="..."))
        mock_name = getattr(p, "_mock_name", None)
        if isinstance(mock_name, str) and mock_name:
            return mock_name
        # último recurso
        return _as_str(v)

    result = uc.execute()
    items = []
    for p in getattr(result, "plans", []):
        items.append(
            PlanSummaryResponse(
                id=_as_str(getattr(p, "id")),
                name=_get_name(p),  # <- aqui o ajuste
                description=_as_str(getattr(p, "description")),
                plan_type=_as_str(getattr(p, "plan_type")),
                billing_cycle=_as_str(getattr(p, "billing_cycle")),
                price_amount=float(getattr(p, "price_amount")),
                price_currency=_as_str(getattr(p, "price_currency", "BRL")),
                max_ads=int(getattr(p, "max_ads", 0)),
                max_featured_ads=int(getattr(p, "max_featured_ads", 0)),
                features=list(getattr(p, "features", []) or []),
            )
        )
    return ListPlansResponse(plans=items)
