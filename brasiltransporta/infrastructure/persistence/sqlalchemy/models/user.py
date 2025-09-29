from __future__ import annotations

from typing import Optional

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.value_objects.email import Email
from brasiltransporta.domain.value_objects.phone_number import PhoneNumber


class UserModel(Base):
    """
    Modelo ORM do usuário.
    - Não expõe regras de negócio; só reflete o armazenamento.
    - Fornece mapeadores de ida/volta com a Entidade de Domínio.
    """

    # __tablename__ é definido automaticamente em Base: "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    birth_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # ISO YYYY-MM-DD
    profession: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    # ---------- mapeadores Domínio <-> Infra ----------

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        """Cria o modelo ORM a partir da Entidade de Domínio."""
        return cls(
            id=user.id,
            name=user.name,
            email=str(user.email),
            password_hash=user.password_hash,
            phone=str(user.phone) if user.phone else None,
            birth_date=user.birth_date,
            profession=user.profession,
            region=user.region,
        )

    def to_domain(self) -> User:
        """Reconstrói a Entidade de Domínio a partir do registro ORM."""
        # Observação: a Entidade User usa fábrica `create(...)` para invariantes,
        # mas aqui reconstruímos diretamente, pois os dados já foram validados na entrada.
        return User(
            id=self.id,
            name=self.name,
            email=Email(self.email),
            password_hash=self.password_hash,
            phone=PhoneNumber(self.phone) if self.phone else None,
            birth_date=self.birth_date,
            profession=self.profession,
            region=self.region,
        )
