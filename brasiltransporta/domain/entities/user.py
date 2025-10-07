# brasiltransporta/domain/entities/user.py
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from brasiltransporta.domain.errors.errors import ValidationError
from brasiltransporta.domain.value_objects.email import Email
from brasiltransporta.domain.value_objects.phone_number import PhoneNumber

@dataclass
class User:
    id: str
    name: str
    email: Email
    password_hash: str
    phone: Optional[PhoneNumber] = None
    birth_date: Optional[str] = None   # ISO "YYYY-MM-DD"
    profession: Optional[str] = None
    region: Optional[str] = None       # ex.: "Sudeste"
    
    # NOVOS CAMPOS PARA AUTENTICAÇÃO
    roles: List[str] = None
    is_active: bool = True
    is_verified: bool = False
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.roles is None:
            self.roles = ["buyer"]  # Role padrão
        
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        password_hash: str,
        phone: Optional[str] = None,
        birth_date: Optional[str] = None,
        profession: Optional[str] = None,
        region: Optional[str] = None,
        roles: List[str] = None
    ) -> "User":
        if not name or len(name.strip()) < 2:
            raise ValidationError("Nome inválido.")
        
        # Validar roles
        valid_roles = ["admin", "seller", "buyer", "moderator"]
        if roles:
            for role in roles:
                if role not in valid_roles:
                    raise ValidationError(f"Role inválida: {role}")
        else:
            roles = ["buyer"]  # Role padrão

        email_vo = Email(email)
        phone_vo = PhoneNumber(phone) if phone else None
        
        return cls(
            id=str(uuid4()),
            name=name.strip(),
            email=email_vo,
            password_hash=password_hash,
            phone=phone_vo,
            birth_date=birth_date,
            profession=profession,
            region=region,
            roles=roles,
            is_active=True,
            is_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    # NOVOS MÉTODOS PARA AUTENTICAÇÃO
    def has_role(self, role: str) -> bool:
        return role in self.roles
    
    def add_role(self, role: str) -> None:
        valid_roles = ["admin", "seller", "buyer", "moderator"]
        if role not in valid_roles:
            raise ValidationError(f"Role inválida: {role}")
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.utcnow()
    
    def remove_role(self, role: str) -> None:
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.utcnow()
    
    def update_last_login(self) -> None:
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def verify(self) -> None:
        self.is_verified = True
        self.updated_at = datetime.utcnow()