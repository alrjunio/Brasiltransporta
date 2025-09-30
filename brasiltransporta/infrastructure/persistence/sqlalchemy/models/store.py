import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base

class StoreModel(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    cnpj = Column(String(18), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

# ... classe StoreModel já existente ...
    vehicles = relationship(
        "VehicleModel",
        back_populates="store",
        cascade="all, delete-orphan"
    )
