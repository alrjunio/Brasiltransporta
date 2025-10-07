from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.errors.errors import ValidationError
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """Implementação concreta do contrato UserRepository usando SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    # ---------------- Comandos ---------------- #

    def add(self, user: User) -> User:
        """Insere um novo usuário e retorna o domínio persistido."""
        email_str = (
            user.email if isinstance(user.email, str)
            else getattr(user.email, "value", str(user.email))
        )
        email_lc = email_str.lower()

        model = UserModel.from_domain(user)
        model.email = email_lc

        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        self._session.commit()
        return model.to_domain()

    def update(self, user: User) -> User:
        """Atualiza campos mutáveis do usuário (last_login, flags, etc)."""
        try:
            user_uuid = uuid.UUID(str(user.id))
        except (ValueError, TypeError):
            raise ValidationError("ID de usuário inválido para update().")

        db_obj = self._session.get(UserModel, user_uuid)
        if not db_obj:
            raise ValidationError("Usuário não encontrado para update().")

        email_str = (
            user.email if isinstance(user.email, str)
            else getattr(user.email, "value", str(user.email))
        )
        email_lc = email_str.lower() if email_str else None

        db_obj.name = user.name
        if email_lc:
            db_obj.email = email_lc
        db_obj.password_hash = user.password_hash
        db_obj.phone = (
            getattr(user.phone, "value", None)
            if user.phone is not None
            else None
        ) or (str(user.phone) if user.phone else None)
        db_obj.birth_date = user.birth_date
        db_obj.profession = user.profession
        db_obj.region = user.region
        db_obj.roles = list(user.roles) if user.roles is not None else []
        db_obj.is_active = bool(user.is_active)
        db_obj.is_verified = bool(user.is_verified)
        db_obj.last_login = user.last_login

        try:
            self._session.add(db_obj)
            self._session.flush()
            self._session.refresh(db_obj)
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise ValidationError("Falha ao atualizar usuário (possível e-mail duplicado).") from e

        return db_obj.to_domain()

    # ---------------- Consultas ---------------- #

    def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_uuid = uuid.UUID(str(user_id))
        except (ValueError, TypeError):
            return None

        stmt = select(UserModel).where(UserModel.id == user_uuid)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        email_str = (
            email if isinstance(email, str)
            else getattr(email, "value", str(email))
        )
        email_lc = email_str.lower()

        stmt = select(UserModel).where(UserModel.email == email_lc)
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.to_domain() if row else None

    def list_by_region(self, region: str, limit: int = 50) -> List[User]:
        stmt = select(UserModel).where(UserModel.region == region).limit(limit)
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def find_by_phone(self, phone: str) -> Optional[User]:
        """Busca usuário pelo número de telefone"""
        try:
            stmt = select(UserModel).where(UserModel.phone == phone)
            row = self._session.execute(stmt).scalar_one_or_none()
            return row.to_domain() if row else None
        except Exception as e:
            print(f"❌ Erro ao buscar usuário por telefone {phone}: {e}")
            return None