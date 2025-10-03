# infrastructure/persistence/sqlalchemy/repositories/advertisement_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from brasiltransporta.domain.entities.advertisement import Advertisement
from brasiltransporta.domain.repositories.advertisement_repository import AdvertisementRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.advertisement import AdvertisementModel

class SQLAlchemyAdvertisementRepository(AdvertisementRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, advertisement: Advertisement) -> None:
        model = AdvertisementModel.from_domain(advertisement)
        self._session.add(model)

    def get_by_id(self, advertisement_id: str) -> Optional[Advertisement]:
        stmt = select(AdvertisementModel).where(AdvertisementModel.id == advertisement_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def list_by_store(self, store_id: str, limit: int = 50) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.store_id == store_id
        ).limit(limit)
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def list_active(self, region: Optional[str] = None, limit: int = 50) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.status == "active"
        ).limit(limit)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def list_featured(self, limit: int = 20) -> List[Advertisement]:
        stmt = select(AdvertisementModel).where(
            AdvertisementModel.status == "active",
            AdvertisementModel.is_featured == True
        ).limit(limit)
        
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def update(self, advertisement: Advertisement) -> None:
        stmt = select(AdvertisementModel).where(AdvertisementModel.id == advertisement.id)
        model = self._session.execute(stmt).scalar_one_or_none()
        if model:
            model.title = advertisement.title
            model.description = advertisement.description
            model.price_amount = advertisement.price.amount
            model.price_currency = advertisement.price.currency
            model.status = advertisement.status.value
            model.is_featured = advertisement.is_featured
            model.views = advertisement.views
            model.updated_at = advertisement.updated_at
