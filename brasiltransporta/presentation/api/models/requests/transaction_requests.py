# presentation/api/models/requests/transaction_requests.py
from pydantic import BaseModel, Field
from typing import Optional, Dict
from brasiltransporta.domain.entities.transaction import PaymentMethod

class CreateTransactionRequest(BaseModel):
    user_id: str = Field(..., description="ID do usuário")
    plan_id: str = Field(..., description="ID do plano")
    amount: float = Field(..., gt=0, description="Valor da transação")
    payment_method: PaymentMethod = Field(..., description="Método de pagamento")
    currency: str = Field("BRL", description="Moeda (padrão: BRL)")
    metadata: Optional[Dict] = Field({}, description="Metadados adicionais")
