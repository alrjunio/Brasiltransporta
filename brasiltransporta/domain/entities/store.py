# brasiltransporta/domain/entities/store.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from brasiltransporta.domain.entities.address import Address
from brasiltransporta.domain.entities.enums import StoreCategory

# No arquivo: ./brasiltransporta/domain/entities/store.py

@dataclass
class Store:
    """Entidade Loja expandida para veículos pesados"""

    # Campos sem valor padrão PRIMEIRO
    id: str
    name: str
    owner_id: str
    description: str
    address: Address
    categories: List[StoreCategory]
    contact_phone: str
    cnpj: str  # ✅ ADICIONAR ESTE CAMPO

    # Campos com valor padrão DEPOIS
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, name: str, owner_id: str, description: str, address: Address,
               categories: List[StoreCategory], contact_phone: str, cnpj: str) -> "Store":  # ✅ ADD CNPJ
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            owner_id=owner_id,
            description=description.strip(),
            address=address,
            categories=categories,
            contact_phone=contact_phone.strip(),
            cnpj=cnpj.strip(),  # ✅ ADD CNPJ
            is_active=True
        )

    @classmethod
    def create_simple(cls, name: str, owner_id: str, cnpj: str) -> "Store":  # ✅ ADD CNPJ
        """Método simplificado para compatibilidade com testes"""
        address = Address.create(
            street="Rua Principal",
            city="São Paulo", 
            state="SP",
            zip_code="01234-567"
        )
        return cls.create(
            name=name,
            owner_id=owner_id,
            description="Loja de veículos",
            address=address,
            categories=[StoreCategory.PARTS_STORE],
            contact_phone="(11) 99999-9999",
            cnpj=cnpj  # ✅ ADD CNPJ
        )
        
        
    def update(self, name: Optional[str] = None, description: Optional[str] = None,
               address: Optional[Address] = None, categories: Optional[List[StoreCategory]] = None,
               contact_phone: Optional[str] = None) -> None:
        if name is not None:
            self.name = name.strip()
        if description is not None:
            self.description = description.strip()
        if address is not None:
            self.address = address
        if categories is not None:
            self.categories = categories
        if contact_phone is not None:
            self.contact_phone = contact_phone.strip()
        self.updated_at = datetime.now(timezone.utc)

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def has_category(self, category: StoreCategory) -> bool:
        return category in self.categories

    def add_category(self, category: StoreCategory) -> None:
        if category not in self.categories:
            self.categories.append(category)
            self.updated_at = datetime.now(timezone.utc)

    def remove_category(self, category: StoreCategory) -> None:
        if category in self.categories:
            self.categories.remove(category)
            self.updated_at = datetime.now(timezone.utc)