import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base

class VehicleModel(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)

    brand = Column(String(80), nullable=False)
    model = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)
    plate = Column(String(10), nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    store = relationship("StoreModel", back_populates="vehicles")
