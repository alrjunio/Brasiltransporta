# presentation/api/models/requests/plan_requests.py
from pydantic import BaseModel, Field
from typing import List, Optional
from brasiltransporta.domain.entities.plan import PlanType, BillingCycle

class CreatePlanRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nome do plano")
    description: str = Field(..., min_length=10, description="Descrição do plano")
    plan_type: PlanType = Field(..., description="Tipo do plano")
    billing_cycle: BillingCycle = Field(..., description="Ciclo de cobrança")
    price_amount: float = Field(..., ge=0, description="Preço do plano")
    price_currency: str = Field("BRL", description="Moeda (padrão: BRL)")
    max_ads: int = Field(10, ge=0, description="Número máximo de anúncios")
    max_featured_ads: int = Field(1, ge=0, description="Número máximo de anúncios em destaque")
    features: Optional[List[str]] = Field([], description="Lista de features do plano")
