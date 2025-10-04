# brasiltransporta/presentation/api/controllers/transactions.py

from dataclasses import asdict, is_dataclass
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

# Schemas (requests/responses)
from brasiltransporta.presentation.api.models.requests.transaction_requests import (
    CreateTransactionRequest,
)
from brasiltransporta.presentation.api.models.responses.transaction_responses import (
    CreateTransactionResponse,
    TransactionDetailResponse,
)

# Use Cases (namespace de transactions)
from brasiltransporta.application.transactions.use_cases.create_transaction import (
    CreateTransactionUseCase,
    CreateTransactionInput,
)
from brasiltransporta.application.transactions.use_cases.get_transaction_by_id import (
    GetTransactionByIdUseCase,
    GetTransactionByIdInput,
)

# DI Providers (ajuste os caminhos se seus providers estiverem em outro módulo)
try:
    from brasiltransporta.presentation.api.di.get_create_transaction_uc import (
        get_create_transaction_uc,
    )
    from brasiltransporta.presentation.api.di.get_get_transaction_by_id_uc import (
        get_get_transaction_by_id_uc,
    )
except Exception:
    # Fallback simples caso não esteja usando DI via Depends no seu projeto:
    get_create_transaction_uc = lambda: CreateTransactionUseCase()  # type: ignore
    get_get_transaction_by_id_uc = lambda: GetTransactionByIdUseCase()  # type: ignore

# Erro de domínio padronizado
try:
    from brasiltransporta.domain.errors.errors import ValidationError
except Exception:
    class ValidationError(Exception):
        pass


router = APIRouter(prefix="/transactions", tags=["transactions"])


def _to_dict(obj: Any) -> Dict[str, Any]:
    """
    Converte dataclass/objeto/DTO em dict, tentando cobrir os formatos
    que os UCs/entidades possam retornar.
    """
    if obj is None:
        return {}

    if isinstance(obj, dict):
        return obj

    if is_dataclass(obj):
        return asdict(obj)

    # tenta ler atributos comuns de entidade Transaction
    possible = {}
    for attr in (
        "id",
        "user_id",
        "plan_id",
        "amount",
        "currency",
        "payment_method",
        "status",
        "external_payment_id",
        "created_at",
        "updated_at",
    ):
        if hasattr(obj, attr):
            possible[attr] = getattr(obj, attr)

    return possible or {"value": obj}


def _normalize_amount_currency(src: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza campos de valor para o schema (float + currency).
    Funciona com ValueObject Money (amount/currency) ou valores simples.
    """
    amount = src.get("amount")
    currency = src.get("currency", "BRL")

    # Se amount for VO Money
    if hasattr(amount, "amount"):
        currency = getattr(amount, "currency", currency)
        amount = getattr(amount, "amount", None)

    # Se amount ainda for um objeto (p.ex. dict)
    if isinstance(amount, dict):
        amount_val = amount.get("amount")
        if amount_val is not None:
            amount = amount_val
        currency = amount.get("currency", currency)

    # garante float se possível
    if amount is not None:
        try:
            amount = float(amount)
        except Exception:
            pass

    return {"amount": amount, "currency": currency}


def _normalize_enum(value: Any) -> str:
    """Converte Enum em string (value)."""
    if hasattr(value, "value"):
        return value.value  # type: ignore
    return str(value) if value is not None else ""


@router.post(
    "",
    response_model=CreateTransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    payload: CreateTransactionRequest,
    uc: CreateTransactionUseCase = Depends(get_create_transaction_uc),
):
    """
    Cria transação via Use Case.
    """
    try:
        # Monta o input do UC a partir do request
        uc_in = CreateTransactionInput(**payload.model_dump())
        created = uc.execute(uc_in)  # entidade/DTO de saída

        data = _to_dict(created)
        amt = _normalize_amount_currency(data)

        return CreateTransactionResponse(
            id=str(data.get("id", "")),
            user_id=str(data.get("user_id", "")),
            plan_id=str(data.get("plan_id", "")),
            amount=amt["amount"],
            currency=amt["currency"],
            payment_method=_normalize_enum(data.get("payment_method")),
            status=_normalize_enum(data.get("status")),
        )
    except ValidationError as ve:
        # erro de domínio => 422
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        ) from ve
    except HTTPException:
        raise
    except Exception as e:
        # Demais erros => 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar transação: {e}",
        ) from e


@router.get(
    "/{transaction_id}",
    response_model=TransactionDetailResponse,
    status_code=status.HTTP_200_OK,
)
def get_transaction_by_id(
    transaction_id: str,
    uc: GetTransactionByIdUseCase = Depends(get_get_transaction_by_id_uc),
):
    """
    Busca transação por ID via Use Case.
    """
    try:
        out = uc.execute(GetTransactionByIdInput(transaction_id=transaction_id))
        if not out:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada.",
            )

        data = _to_dict(out)
        amt = _normalize_amount_currency(data)

        return TransactionDetailResponse(
            id=str(data.get("id", "")),
            user_id=str(data.get("user_id", "")),
            plan_id=str(data.get("plan_id", "")),
            amount=amt["amount"],
            currency=amt["currency"],
            payment_method=_normalize_enum(data.get("payment_method")),
            status=_normalize_enum(data.get("status")),
            external_payment_id=data.get("external_payment_id"),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar transação: {e}",
        ) from e
