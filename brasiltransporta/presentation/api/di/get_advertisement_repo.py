from fastapi import Depends
from sqlalchemy.orm import Session

# sua factory de sessão SQLAlchemy
from brasiltransporta.infrastructure.persistence.sqlalchemy.session import get_session

# repositório real dos anúncios (ajuste o caminho se o seu arquivo tiver outro nome/pasta)
from brasiltransporta.infrastructure.persistence.sqlalchemy.repositories.advertisement_repository import (
    SQLAlchemyAdvertisementRepository,
)

def get_advertisement_repo(
    db: Session = Depends(get_session),
) -> SQLAlchemyAdvertisementRepository:
    """
    Provider simples que injeta a Session e devolve o repositório SQLAlchemy.
    Use-o nos controllers com: repo = Depends(get_advertisement_repo)
    """
    return SQLAlchemyAdvertisementRepository(db)
