import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, String, Text, DateTime, Numeric, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class AdvertisementModel(Base):
    __tablename__ = "advertisements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price_amount = Column(Numeric(12, 2), nullable=False)
    price_currency = Column(String(3), nullable=False, default="BRL")
    status = Column(String(20), nullable=False, default="draft")
    is_featured = Column(Boolean, nullable=False, default=False)
    views = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
