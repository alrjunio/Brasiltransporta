# brasiltransporta/infrastructure/persistence/sqlalchemy/models/user_model.py
from __future__ import annotations
from uuid import uuid4
from sqlalchemy import String, DateTime, Boolean, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
from brasiltransporta.domain.entities.user import User

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # NOVOS CAMPOS PARA AUTENTICAÇÃO
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    birth_date: Mapped[str | None] = mapped_column(String(10), nullable=True)  # YYYY-MM-DD
    profession: Mapped[str | None] = mapped_column(String(100), nullable=True)
    region: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # CAMPOS DE AUTENTICAÇÃO E ROLES
    roles: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_login: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # ---- mapeamentos domínio <-> ORM ----
    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        email_str = (
            user.email if isinstance(user.email, str)
            else getattr(user.email, "value", str(user.email))
        )
        
        phone_str = (
            user.phone.value if user.phone and hasattr(user.phone, 'value')
            else str(user.phone) if user.phone else None
        )
        
        return cls(
            id=user.id,
            name=user.name,
            email=email_str,
            password_hash=user.password_hash,
            phone=phone_str,
            birth_date=user.birth_date,
            profession=user.profession,
            region=user.region,
            roles=user.roles,
            is_active=user.is_active,
            is_verified=user.is_verified,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def to_domain(self) -> User:
        from brasiltransporta.domain.value_objects.email import Email
        from brasiltransporta.domain.value_objects.phone_number import PhoneNumber
        
        return User(
            id=str(self.id),
            name=self.name,
            email=Email(self.email),
            password_hash=self.password_hash,
            phone=PhoneNumber(self.phone) if self.phone else None,
            birth_date=self.birth_date,
            profession=self.profession,
            region=self.region,
            roles=self.roles,
            is_active=self.is_active,
            is_verified=self.is_verified,
            last_login=self.last_login,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )