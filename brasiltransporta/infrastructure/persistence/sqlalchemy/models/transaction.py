import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="BRL")
    payment_method = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    external_payment_id = Column(String(100), nullable=True)
    payment_metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
