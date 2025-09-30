# presentation/api/routes/transactions.py
from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

from brasiltransporta.presentation.api.models.requests.transaction_requests import CreateTransactionRequest
from brasiltransporta.presentation.api.models.responses.transaction_responses import (
    CreateTransactionResponse,
    TransactionDetailResponse,
)

from brasiltransporta.application.transactions.use_cases.create_transaction import (
    CreateTransactionUseCase,
    CreateTransactionInput,
)
from brasiltransporta.application.transactions.use_cases.get_transaction_by_id import (
    GetTransactionByIdUseCase,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=CreateTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: CreateTransactionRequest,
    uc: CreateTransactionUseCase = Depends(),  # DI provider necessário
):
    try:
        out = uc.execute(CreateTransactionInput(**payload.model_dump()))
        return CreateTransactionResponse(id=out.transaction_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@router.get("/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction_by_id(
    transaction_id: str,
    uc: GetTransactionByIdUseCase = Depends(),  # DI provider necessário
):
    out = uc.execute(transaction_id)
    if out is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada."
        )
    return TransactionDetailResponse(**asdict(out))
