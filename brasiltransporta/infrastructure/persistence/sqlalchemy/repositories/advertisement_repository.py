# infrastructure/persistence/sqlalchemy/repositories/advertisement_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.entities.enums import AdvertisementStatus
from brasiltransporta.domain.repositories.advertisement_repository import AdvertisementRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.advertisement import AdvertisementModel

class SQLAlchemyAdvertisementRepository(AdvertisementRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    # --- MÉTODOS PRINCIPAIS (compatíveis com interface) ---
    async def create(self, advertisement: Advertisement) -> Advertisement:
        """Cria um novo anúncio (substitui add)"""
        model = AdvertisementModel.from_domain(advertisement)
        self._session.add(model)
        self._session.commit()
        return model.to_domain()

    async def get_by_id(self, advertisement_id: str) -> Optional[Advertisement]:
        stmt = select(AdvertisementModel).where(AdvertisementModel.id == advertisement_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    async def update(self, advertisement: Advertisement) -> Advertisement:
        """Atualiza todos os campos do anúncio"""
        stmt = select(AdvertisementModel).where(AdvertisementModel.id == advertisement.id)
        model = self._session.execute(stmt).scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Advertisement {advertisement.id} not found")
        
        # Atualiza todos os campos
        model.title = advertisement.title
        model.description = advertisement.description
        model.price_amount = float(advertisement.price)  # ← Converte Decimal para float
        model.price_currency = advertisement.price_currency
        model.status = advertisement.status.value  # ← Usa .value do Enum
        model.is_featured = advertisement.is_featured
        model.views = advertisement.views
        model.images = advertisement.images  # ← NOVO CAMPO
        model.videos = advertisement.videos  # ← NOVO CAMPO
        model.expires_at = advertisement.expires_at  # ← NOVO CAMPO
        model.updated_at = advertisement.updated_at
        
        self._session.commit()
        return model.to_domain()

    async def delete(self, advertisement_id: str) -> bool:
        stmt = select(AdvertisementModel).where(AdvertisementModel.id == advertisement_id)
        model = self._session.execute(stmt).scalar_one_or_none()
        
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False

    # --- MÉTODOS DE CONSULTA ---
    async def list_by_store(self, store_id: str, limit: int = 50) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.store_id == store_id
        ).limit(limit)
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    async def list_by_vehicle(self, vehicle_id: str) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.vehicle_id == vehicle_id
        )
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    async def list_by_status(self, status: AdvertisementStatus) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.status == status.value  # ← Usa Enum
        )
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    async def list_active(self, region: Optional[str] = None, limit: int = 50) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.status == AdvertisementStatus.ACTIVE.value  # ← Corrigido
        ).limit(limit)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    async def list_featured(self, limit: int = 20) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.status == AdvertisementStatus.ACTIVE.value,  # ← Corrigido
            AdvertisementModel.is_featured == True
        ).limit(limit)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    # --- NOVOS MÉTODOS PARA MÍDIA ---
    async def update_images(self, advertisement_id: str, images: List[str]) -> bool:
        stmt = update(AdvertisementModel).where(
            AdvertisementModel.id == advertisement_id
        ).values(images=images)
        
        result = self._session.execute(stmt)
        self._session.commit()
        return result.rowcount > 0

    async def update_videos(self, advertisement_id: str, videos: List[str]) -> bool:
        stmt = update(AdvertisementModel).where(
            AdvertisementModel.id == advertisement_id
        ).values(videos=videos)
        
        result = self._session.execute(stmt)
        self._session.commit()
        return result.rowcount > 0

    async def increment_views(self, advertisement_id: str) -> bool:
        stmt = update(AdvertisementModel).where(
            AdvertisementModel.id == advertisement_id
        ).values(views=AdvertisementModel.views + 1)
        
        result = self._session.execute(stmt)
        self._session.commit()
        return result.rowcount > 0

    async def search_ads(self, query: str, category: Optional[str] = None) -> List[Advertisement]:
        search_term = f"%{query}%"
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.title.ilike(search_term) |
            AdvertisementModel.description.ilike(search_term)
        )
        
        # TODO: Implementar filtro por categoria quando tivermos categorias de veículos
        if category:
            stmt = stmt.where(AdvertisementModel.status == AdvertisementStatus.ACTIVE.value)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]