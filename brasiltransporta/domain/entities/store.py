from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Optional


@dataclass
class Store:
    id: str
    name: str
    owner_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, name: str, owner_id: str) -> "Store":
        return cls(id=str(uuid4()), name=name, owner_id=owner_id)
