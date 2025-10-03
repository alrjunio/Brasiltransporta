from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

# Schemas (use os seus)
from brasiltransporta.presentation.api.models.requests.transaction_requests import CreateTransactionRequest
from brasiltransporta.presentation.api.models.responses.transaction_responses import (
    CreateTransactionResponse,
    TransactionDetailResponse,
)

# Use Cases (ajuste o caminho se seus UCs estiverem em outro namespace)
from brasiltransporta.application.billing.use_cases.create_transaction import (
    CreateTransactionUseCase,
    CreateTransactionInput,
)
from brasiltransporta.application.billing.use_cases.get_transaction_by_id import (
    GetTransactionByIdUseCase,
)

# Providers (DI)
from brasiltransporta.presentation.api.di.get_create_transaction_uc import get_create_transaction_uc
from brasiltransporta.presentation.api.di.get_get_transaction_by_id_uc import get_get_transaction_by_id_uc

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=CreateTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: CreateTransactionRequest,
    uc: CreateTransactionUseCase = Depends(get_create_transaction_uc),
):
    """
    Cria transação chamando o Use Case via DI.
    """
    try:
        out = uc.execute(CreateTransactionInput(**payload.model_dump()))
        return CreateTransactionResponse(id=out.transaction_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.get("/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction_by_id(
    transaction_id: str,
    uc: GetTransactionByIdUseCase = Depends(get_get_transaction_by_id_uc),
):
    """
    Busca transação por ID via Use Case (nada de Repository na assinatura).
    """
    out = uc.execute(transaction_id)
    if out is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada.")
    return TransactionDetailResponse(**asdict(out))
