# brasiltransporta/domain/entities/advertisement.py
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional
from uuid import uuid4
from enum import Enum

from brasiltransporta.domain.entities.enums import AdvertisementStatus


@dataclass
class Advertisement:
    """Entidade Anúncio expandida mantendo compatibilidade"""
    
    id: str
    store_id: str
    vehicle_id: str
    title: str
    description: str
    price_amount: float
    
    price_currency: str = "BRL"
    status: AdvertisementStatus = AdvertisementStatus.DRAFT
    is_featured: bool = False
    views: int = 0
    images: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Garante compatibilidade entre price_amount e price"""
        self.price = Decimal(str(self.price_amount))

    @classmethod
    def create(
        cls,
        store_id: str,
        vehicle_id: str,
        title: str,
        description: Optional[str] = "",
        price_amount: float = 0.0,
        price_currency: str = "BRL",
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None
    ) -> "Advertisement":
        # VALIDAÇÕES EXISTENTES (para compatibilidade com testes):
        if len(title) < 5:
            raise ValueError("Título deve ter pelo menos 5 caracteres")
        if len(description) < 10:
            raise ValueError("Descrição deve ter pelo menos 10 caracteres")
        if price_amount <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        return cls(
            id=str(uuid4()),
            store_id=store_id,
            vehicle_id=vehicle_id,
            title=title,
            description=description or "",
            price_amount=float(price_amount),
            price_currency=price_currency,
            status=AdvertisementStatus.DRAFT,
            is_featured=False,
            views=0,
            images=images or [],
            videos=videos or []
        )

    def publish(self) -> None:
        if self.status != AdvertisementStatus.DRAFT:
            raise ValueError("Apenas anúncios em rascunho podem ser publicados")
        self.status = AdvertisementStatus.ACTIVE
        self.expires_at = datetime.utcnow() + timedelta(days=30)
        self.updated_at = datetime.utcnow()

    def mark_as_sold(self) -> None:
        self.status = AdvertisementStatus.SOLD
        self.updated_at = datetime.utcnow()

    def increment_views(self) -> None:
        self.views += 1
        self.updated_at = datetime.utcnow()

    def pause(self) -> None:
        """Pausa o anúncio"""
        if self.status == AdvertisementStatus.ACTIVE:
            self.status = AdvertisementStatus.PAUSED
            self.updated_at = datetime.utcnow()

    def resume(self) -> None:
        """Retoma um anúncio pausado"""
        if self.status == AdvertisementStatus.PAUSED:
            self.status = AdvertisementStatus.ACTIVE
            self.updated_at = datetime.utcnow()

    def add_image(self, image_url: str) -> None:
        """Adiciona uma imagem ao anúncio"""
        self.images.append(image_url)
        self.updated_at = datetime.utcnow()

    def add_video(self, video_url: str) -> None:
        """Adiciona um vídeo ao anúncio"""
        self.videos.append(video_url)
        self.updated_at = datetime.utcnow()

    def set_featured(self, featured: bool) -> None:
        """Define se o anúncio é destacado"""
        self.is_featured = featured
        self.updated_at = datetime.utcnow()

    def is_expired(self) -> bool:
        """Verifica se o anúncio expirou"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def renew(self, days: int = 30) -> None:
        """Renova o anúncio por mais dias"""
        if self.status == AdvertisementStatus.ACTIVE:
            self.expires_at = datetime.utcnow() + timedelta(days=days)
            self.updated_at = datetime.utcnow()

    @property
    def has_media(self) -> bool:
        """Verifica se o anúncio tem mídia"""
        return len(self.images) > 0 or len(self.videos) > 0