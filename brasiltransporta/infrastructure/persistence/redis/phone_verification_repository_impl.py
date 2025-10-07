# CORRIGIR brasiltransporta/infrastructure/persistence/redis/phone_verification_repository_impl.py
import json
from typing import Optional
from datetime import datetime
from brasiltransporta.domain.entities.phone_verification import PhoneVerification
from brasiltransporta.domain.repositories.phone_verification_repository import PhoneVerificationRepository
import redis

class RedisPhoneVerificationRepository(PhoneVerificationRepository):
    def __init__(self, redis_client: redis.Redis = None):
        self.redis = redis_client or redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        self.prefix = "phone_verification:"
    
    def _get_key(self, phone: str) -> str:
        return f"{self.prefix}{phone}"
    
    def save(self, verification: PhoneVerification) -> None:
        key = self._get_key(verification.phone)
        data = {
            'phone': verification.phone,
            'code': verification.code,
            'created_at': verification.created_at.isoformat(),
            'expires_at': verification.expires_at.isoformat(),
            'used': verification.used
        }
        # Expira em 10 minutos (mesmo tempo da entidade)
        self.redis.setex(key, 600, json.dumps(data))
    
    def get_by_phone(self, phone: str) -> Optional[PhoneVerification]:
        key = self._get_key(phone)
        data = self.redis.get(key)
        if not data:
            return None
        
        data_dict = json.loads(data)
        # ✅ CORRIGIR: Converter strings ISO de volta para datetime
        verification = PhoneVerification(
            phone=data_dict['phone'],
            code=data_dict['code'],
            created_at=datetime.fromisoformat(data_dict['created_at']),  # CONVERTER
            expires_at=datetime.fromisoformat(data_dict['expires_at']),  # CONVERTER  
            used=data_dict['used']
        )
        return verification
    
    def delete_by_phone(self, phone: str) -> None:
        key = self._get_key(phone)
        self.redis.delete(key)