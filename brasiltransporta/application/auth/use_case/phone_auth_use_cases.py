# 📄 brasiltransporta/application/auth/use_cases/phone_auth_use_cases.py
from typing import Tuple, Optional
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.entities.phone_verification import PhoneVerification
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.domain.repositories.phone_verification_repository import PhoneVerificationRepository
from brasiltransporta.application.auth.use_case.phone_auth_inputs import (
    SendPhoneVerificationCodeCommand, 
    VerifyPhoneCodeCommand,
    PhoneLoginCommand
)
from brasiltransporta.infrastructure.external.sms.sms_service import SMSService

class SendPhoneVerificationUseCase:
    def __init__(
        self,
        verification_repo: PhoneVerificationRepository,
        sms_service: SMSService
    ):
        self.verification_repo = verification_repo
        self.sms_service = sms_service

    async def execute(self, command: SendPhoneVerificationCodeCommand) -> bool:
        # Remove verificações anteriores do mesmo número
        self.verification_repo.delete_by_phone(command.phone)
        
        # Cria nova verificação
        verification = PhoneVerification.create(command.phone)
        self.verification_repo.save(verification)
        
        # Envia SMS (mock em desenvolvimento)
        return await self.sms_service.send_verification_code(
            command.phone, 
            verification.code
        )

class VerifyPhoneCodeUseCase:
    def __init__(
        self,
        verification_repo: PhoneVerificationRepository,
        user_repo: UserRepository
    ):
        self.verification_repo = verification_repo
        self.user_repo = user_repo

    async def execute(self, command: VerifyPhoneCodeCommand) -> Tuple[bool, Optional[User]]:
        verification = self.verification_repo.get_by_phone(command.phone)
        
        if not verification:
            return False, None
            
        if not verification.verify_code(command.code):
            return False, None
            
        # Marca como usado
        verification.mark_as_used()
        self.verification_repo.save(verification)
        
        # Busca usuário pelo telefone
        user =  self._find_user_by_phone(command.phone)
        return True, user

    def _find_user_by_phone(self, phone: str) -> Optional[User]:
        # Precisamos adicionar este método no UserRepository primeiro
        # Por enquanto, retorna None - usuário precisa se cadastrar
        return None