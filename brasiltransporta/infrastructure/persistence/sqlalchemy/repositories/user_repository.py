from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.user import UserModel
from brasiltransporta.domain.errors.errors import ValidationError


class SQLAlchemyUserRepository(UserRepository):
    """Implementação concreta do contrato UserRepository usando SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------- comandos -------

    def add(self, user: User) -> User:
        model = UserModel.from_domain(user)
        self._session.add(model)
        self._session.flush()   # garante PK gerada
        self._session.refresh(model)
        self._session.commit() 
        return model.to_domain()

    # ------- consultas -------

    def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        email_str = (
        email if isinstance(email, str)
        else getattr(email, "value", str(email))
    )
        stmt = select(UserModel).where(UserModel.email == email.lower())
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def list_by_region(self, region: str, limit: int = 50) -> List[User]:
        stmt = select(UserModel).where(UserModel.region == region).limit(limit)
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

