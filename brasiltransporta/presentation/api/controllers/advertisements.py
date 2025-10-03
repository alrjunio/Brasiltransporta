from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

# ================== Schemas ==================
# Se você já tem estes schemas, os imports abaixo funcionarão.
# Se ainda não tiver, o bloco "fallback" evita quebrar a aplicação.
try:
    from brasiltransporta.presentation.api.models.requests.advertisement_requests import (
        CreateAdvertisementRequest,
        PublishAdvertisementRequest,  # opcional, se o publish tiver corpo
    )
    from brasiltransporta.presentation.api.models.responses.advertisement_responses import (
        CreateAdvertisementResponse,
        AdvertisementDetailResponse,
        PublishAdvertisementResponse,
    )
except Exception:
    from pydantic import BaseModel
    from typing import Optional, Dict

    class CreateAdvertisementRequest(BaseModel):
        store_id: str
        title: str
        description: str
        price_amount: float
        price_currency: str = "BRL"
        metadata: Optional[Dict] = None

    class PublishAdvertisementRequest(BaseModel):
        featured: bool | None = None

    class CreateAdvertisementResponse(BaseModel):
        id: str

    class PublishAdvertisementResponse(BaseModel):
        id: str
        status: str

    class AdvertisementDetailResponse(BaseModel):
        id: str
        store_id: str
        title: str
        description: str
        price_amount: float
        price_currency: str
        status: str
        metadata: Dict = {}
        created_at: str
        updated_at: str | None = None

# ================== DI / Providers ==================
# Este provider deve existir em: presentation/api/di/get_advertisement_repo.py
from brasiltransporta.presentation.api.di.get_advertisement_repo import get_advertisement_repo

router = APIRouter(prefix="/advertisements", tags=["advertisements"])


@router.post("", response_model=CreateAdvertisementResponse, status_code=status.HTTP_201_CREATED)
def create_advertisement(
    payload: CreateAdvertisementRequest,
    repo = Depends(get_advertisement_repo),  # ✅ NÃO tipar Repository aqui
):
    """
    Cria um anúncio. Se você preferir, troque o repo por um Use Case via Depends.
    """
    # Tenta métodos comuns; ajuste se o seu repositório tiver outro nome/assinatura.
    # 1) create(payload_dict)
    if hasattr(repo, "create"):
        try:
            new_id = repo.create(payload.model_dump())
            return CreateAdvertisementResponse(id=str(new_id))
        except TypeError:
            pass  # pode esperar uma entidade em vez de dict

    # 2) add(entity) — se o repo trabalha com entidade de domínio
    if hasattr(repo, "add"):
        try:
            new_id = repo.add(payload.model_dump())  # ajuste se precisar instanciar entidade
            return CreateAdvertisementResponse(id=str(new_id))
        except TypeError:
            pass

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Repositório de anúncios não possui método de criação suportado (ajuste para usar o seu UC ou repo real).",
    )


@router.get("/{advertisement_id}", response_model=AdvertisementDetailResponse)
def get_advertisement_by_id(
    advertisement_id: str,
    repo = Depends(get_advertisement_repo),  # ✅
):
    """
    Retorna um anúncio por ID.
    """
    model = None
    for method_name in ("get_by_id", "find_by_id"):
        if hasattr(repo, method_name):
            model = getattr(repo, method_name)(advertisement_id)
            break

    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Anúncio não encontrado.")

    # Mapeia para o response — ajuste campos conforme sua entidade/ORM.
    try:
        return AdvertisementDetailResponse(
            id=str(getattr(model, "id")),
            store_id=str(getattr(model, "store_id")),
            title=getattr(model, "title"),
            description=getattr(model, "description"),
            price_amount=float(getattr(model, "price_amount")),
            price_currency=str(getattr(model, "price_currency", "BRL")),
            status=str(getattr(model, "status")),
            metadata=getattr(model, "metadata", {}) or {},
            created_at=getattr(model, "created_at"),
            updated_at=getattr(model, "updated_at", None),
        )
    except Exception:
        # fallback: tenta dicionário/objeto genérico
        data = model if isinstance(model, dict) else getattr(model, "__dict__", {})
        return AdvertisementDetailResponse(**data)


@router.post("/{advertisement_id}/publish", response_model=PublishAdvertisementResponse)
def publish_advertisement(
    advertisement_id: str,
    payload: PublishAdvertisementRequest | None = None,
    repo = Depends(get_advertisement_repo),  # ✅ aqui era onde dava o erro — agora com Depends
):
    """
    Publica o anúncio. Se tiver Use Case de publicação, injete o UC via Depends e use aqui.
    """
    # 1) publish(id, **kwargs)
    if hasattr(repo, "publish"):
        getattr(repo, "publish")(advertisement_id, **(payload.model_dump() if payload else {}))
        return PublishAdvertisementResponse(id=advertisement_id, status="published")

    # 2) update_status(id, 'published') / set_status(id, 'published')
    for method_name in ("update_status", "set_status"):
        if hasattr(repo, method_name):
            getattr(repo, method_name)(advertisement_id, status="published")
            return PublishAdvertisementResponse(id=advertisement_id, status="published")

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Repositório de anúncios não possui operação de publicação (crie o UC ou implemente no repo).",
    )
