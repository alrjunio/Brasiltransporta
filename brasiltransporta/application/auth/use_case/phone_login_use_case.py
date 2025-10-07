# CORRIGIR brasiltransporta/application/auth/use_case/phone_login_use_case.py
from typing import Optional, Tuple
from brasiltransporta.domain.entities.user import User
from brasiltransporta.domain.repositories.user_repository import UserRepository
from brasiltransporta.domain.repositories.phone_verification_repository import PhoneVerificationRepository
from brasiltransporta.application.auth.use_case.phone_auth_inputs import PhoneLoginCommand
from brasiltransporta.infrastructure.security.jwt_service import JWTService  # ✅ ADICIONAR

class PhoneLoginUseCase:
    def __init__(
        self,
        verification_repo: PhoneVerificationRepository,
        user_repo: UserRepository,
        jwt_service: JWTService  
    ):
        self.verification_repo = verification_repo
        self.user_repo = user_repo
        self.jwt_service = jwt_service  

    async def execute(self, command: PhoneLoginCommand) -> Tuple[Optional[User], Optional[str]]:
        # 1. Verificar código
        verification = self.verification_repo.get_by_phone(command.phone)
        if not verification:
            return None, "Código não encontrado"
            
        if not verification.verify_code(command.code):
            return None, "Código inválido ou expirado"
            
        # 2. Buscar usuário
        user = self.user_repo.find_by_phone(command.phone)
        if not user:
            return None, "Usuário não encontrado"
            
        # 3. Marcar verificação como usada
        verification.mark_as_used()
        self.verification_repo.save(verification)
        
        return user, None