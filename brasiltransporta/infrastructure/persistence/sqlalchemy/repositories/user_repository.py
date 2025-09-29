from __future__ import annotations

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.user import UserModel
from brasiltransporta.domain.errors import ValidationError


class SQLAlchemyUserRepository(UserRepository):
    """Implementação concreta do contrato UserRepository usando SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------- comandos -------

    def add(self, user: User) -> None:
        model = UserModel.from_domain(user)
        self._session.add(model)
        try:
            # flush para materializar possíveis constraints antes do commit (ex.: unique)
            self._session.flush()
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            # Ex.: violação de uq_user_email -> traduz para erro de domínio (422 via FastAPI)
            raise ValidationError("E-mail já cadastrado.") from e

    # ------- consultas -------

    def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email.lower())
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def list_by_region(self, region: str, limit: int = 50) -> List[User]:
        stmt = select(UserModel).where(UserModel.region == region).limit(limit)
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]
