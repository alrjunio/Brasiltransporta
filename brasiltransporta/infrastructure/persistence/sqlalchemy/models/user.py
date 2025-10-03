# brasiltransporta/infrastructure/persistence/sqlalchemy/models/user_model.py
from __future__ import annotations
from uuid import uuid4
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
from brasiltransporta.domain.entities.user import User  # ajuste o caminho se diferente

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)  # ajuste se seu domínio usar outro nome
    region: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # ---- mapeamentos domínio <-> ORM ----
    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
         # Garanta que email seja string
        email_str = (
            user.email if isinstance(user.email, str)
            else getattr(user.email, "value", str(user.email))
        )
        
        return cls(
            id=user.id,
            name=user.name,
            email=str(user.email),
            password_hash=user.password_hash,  # se no domínio for 'hashed_password', mude aqui
            region=user.region,
           
        )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            password_hash=self.password_hash,  # idem comentário acima
            region=self.region,
            #created_at=self.created_at,
            #updated_at=self.updated_at,
        )
