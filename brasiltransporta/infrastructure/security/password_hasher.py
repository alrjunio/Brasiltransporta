from __future__ import annotations
from passlib.hash import bcrypt # type: ignore
from brasiltransporta.application.users.use_cases.register_user import PasswordHasher

class BcryptPasswordHasher(PasswordHasher):  # Agora implementa a interface
    """Implementação real de hashing de senha usando passlib/bcrypt."""

    def hash(self, raw_password: str) -> str:
        if not raw_password or len(raw_password) < 6:
            # regra simples de segurança mínima; ajuste conforme sua política
            raise ValueError("Senha deve ter pelo menos 6 caracteres.")
        return bcrypt.hash(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        """Útil para fluxos de login/autenticação (opcional aqui)."""
        return bcrypt.verify(raw_password, hashed_password)