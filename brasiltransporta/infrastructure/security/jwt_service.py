from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import jwt, JWTError

# Tentamos obter configurações sem “quebrar” se algum campo não existir
try:
    from brasiltransporta.infrastructure.config.settings import AppSettings
except Exception:  # pragma: no cover
    AppSettings = None  # type: ignore[misc]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class JWTService:
    """
    Serviço de emissão e verificação de JWT com hardening:
      - iss, aud opcionais (se configurados)
      - iat, nbf, exp
      - jti
      - (leeway removido do decode por incompatibilidade da lib no ambiente)
    """

    def __init__(self) -> None:
        defaults = {
            "secret_key": "change-me-in-production",
            "algorithm": "HS256",
            "access_minutes": 30,
            "refresh_days": 7,
            "issuer": None,          # ex.: "brasiltransporta"
            "audience": None,        # ex.: "brasiltransporta.api"
            "leeway_seconds": 30,    # mantido, mas não passado ao decode
        }

        # ✅ Primeiro, tenta pegar diretamente do ambiente
        import os
        env_secret = os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY")

        if AppSettings is not None:
            app = AppSettings()
            auth = getattr(app, "auth", None)

            # ✅ Prioriza o segredo do ambiente
            self._secret = (
                env_secret
                or getattr(auth, "secret_key", None)
                or getattr(app, "secret_key", None)
                or defaults["secret_key"]
            )
            self._alg = (
                getattr(auth, "algorithm", None)
                or getattr(app, "algorithm", None)
                or defaults["algorithm"]
            )
            self._access_minutes = int(
                getattr(auth, "access_token_exp_minutes", None)
                or getattr(app, "access_token_exp_minutes", None)
                or defaults["access_minutes"]
            )
            self._refresh_days = int(
                getattr(auth, "refresh_token_exp_days", None)
                or getattr(app, "refresh_token_exp_days", None)
                or defaults["refresh_days"]
            )
            self._issuer: Optional[str] = (
                getattr(auth, "issuer", None)
                or getattr(app, "issuer", None)
                or defaults["issuer"]
            )
            self._audience: Optional[str] = (
                getattr(auth, "audience", None)
                or getattr(app, "audience", None)
                or defaults["audience"]
            )
            self._leeway = int(
                getattr(auth, "leeway_seconds", None)
                or getattr(app, "leeway_seconds", None)
                or defaults["leeway_seconds"]
            )
        else:
            # fallback total se AppSettings falhar
            self._secret = env_secret or defaults["secret_key"]
            self._alg = defaults["algorithm"]
            self._access_minutes = defaults["access_minutes"]
            self._refresh_days = defaults["refresh_days"]
            self._issuer = defaults["issuer"]
            self._audience = defaults["audience"]
            self._leeway = defaults["leeway_seconds"]

    def verify_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify refresh token specifically - check type and signature"""
        try:
            payload = self.verify_token(token)  # Usa o método existente
            if payload and payload.get("type") == "refresh":
                return payload
            return None
        except Exception:
            return None

    def verify_token_with_type(self, token: str, expected_type: str) -> Optional[Dict[str, Any]]:
        """
        Verifica token e valida o tipo esperado
        """
        payload = self.verify_token(token)
        if not payload:
            return None
            
        token_type = payload.get("type")
        if token_type != expected_type:
            return None
            
        return payload
    
    def create_refresh_token_with_family(self, claims: Dict[str, Any], token_family: str) -> str:
        """
        Cria refresh token incluindo a família para rastreamento
        """
        claims_with_family = claims.copy()
        claims_with_family["token_family"] = token_family
        return self.create_refresh_token(claims_with_family)

    # ---------------------------
    # Public API
    # ---------------------------

    def create_access_token(self, claims: Dict[str, Any]) -> str:
        return self._create_token(claims=claims, minutes=self._access_minutes, token_type="access")

    def create_refresh_token(self, claims: Dict[str, Any]) -> str:
        return self._create_token(claims=claims, days=self._refresh_days, token_type="refresh")

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica assinatura e validade (exp/nbf/iat) e, se configurados, iss/aud.
        Retorna o payload (dict) se válido; caso contrário, retorna None.
        """
        if not token or not isinstance(token, str):
            return None

        options = {
            "require": ["exp", "iat", "nbf", "jti", "type"],
            "verify_exp": True,
            "verify_signature": True,
        }

        kwargs: Dict[str, Any] = {
            "algorithms": [self._alg],
            "options": options,
            # REMOVIDO: 'leeway' — a lib do ambiente não aceita esse kwarg
        }
        if self._issuer:
            kwargs["issuer"] = self._issuer
        if self._audience:
            kwargs["audience"] = self._audience

        try:
            data = jwt.decode(token, self._secret, **kwargs)
            if "email" in data and not isinstance(data["email"], str):
                data["email"] = str(data["email"])
            return data
        except Exception:
            # PyJWTError / JOSEError / etc -> inválido
            return None

    # ---------------------------
    # Internals
    # ---------------------------

    def _create_token(
        self,
        *,
        claims: Dict[str, Any],
        token_type: str,
        minutes: Optional[int] = None,
        days: Optional[int] = None,
    ) -> str:
        now = _utcnow()

        sub = claims.get("sub")
        email = claims.get("email")
        roles = claims.get("roles", [])

        payload: Dict[str, Any] = {
            "sub": str(sub) if sub is not None else None,
            "email": str(email) if email is not None else None,
            "roles": list(roles) if isinstance(roles, (list, tuple)) else [],
            "type": token_type,
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "jti": str(uuid.uuid4()),
        }

        if minutes is not None:
            exp = now + timedelta(minutes=minutes)
        elif days is not None:
            exp = now + timedelta(days=days)
        else:
            exp = now + timedelta(minutes=30)

        payload["exp"] = int(exp.timestamp())

        if self._issuer:
            payload["iss"] = self._issuer
        if self._audience:
            payload["aud"] = self._audience

        payload = {k: v for k, v in payload.items() if v is not None}

        token = jwt.encode(payload, self._secret, algorithm=self._alg)
        return token