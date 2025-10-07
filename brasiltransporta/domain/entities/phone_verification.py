# Entidade PhoneVerification corrigida
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class PhoneVerification:
    phone: str
    code: str
    created_at: datetime
    expires_at: datetime
    used: bool = False  # ✅ ADICIONAR ESTE ATRIBUTO
    
    @classmethod
    def create(cls, phone: str) -> 'PhoneVerification':
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=10)
        return cls(
            phone=phone,
            code=code,
            created_at=created_at,
            expires_at=expires_at,
            used=False
        )
    
    def verify_code(self, code: str) -> bool:
        if self.used:
            return False
        if datetime.now() > self.expires_at:
            return False
        return self.code == code
    
    def mark_as_used(self) -> None:
        self.used = True