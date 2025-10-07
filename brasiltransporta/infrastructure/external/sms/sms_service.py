# 📄 brasiltransporta/infrastructure/sms/sms_service.py
from typing import Protocol
import logging

logger = logging.getLogger(__name__)

class SMSService(Protocol):
    async def send_verification_code(self, phone: str, code: str) -> bool: ...

class MockSMSService:
    """Serviço mock para desenvolvimento"""
    
    async def send_verification_code(self, phone: str, code: str) -> bool:
        logger.info(f"📱 SMS Mock - Código de verificação para {phone}: {code}")
        print(f"🔐 Código de verificação para {phone}: {code}")
        return True

class TwilioSMSService:
    """Implementação real com Twilio (para produção)"""
    
    async def send_verification_code(self, phone: str, code: str) -> bool:
        # TODO: Implementar com Twilio
        try:
            # from twilio.rest import Client
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(...)
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar SMS: {e}")
            return False