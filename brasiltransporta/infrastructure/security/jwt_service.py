from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, List

from jose import jwt, JWTError

# Tentamos importar AppSettings, mas não obrigamos a existir.
try:
    from brasiltransporta.infrastructure.config.settings import AppSettings
except Exception:
    AppSettings = None  # type: ignore


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class JWTService:
    """
    Serviço de criação e verificação de JWTs (access e refresh).
    Não possui dependência de repositórios. Apenas assina e valida tokens.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_exp_minutes: int = 60,
        refresh_token_exp_days: int = 7,
        issuer: Optional[str] = None,
        audience: Optional[str] = None,
    ) -> None:
        if not secret_key:
            raise ValueError("secret_key é obrigatório")
        self._secret = secret_key
        self._alg = algorithm or "HS256"
        self._access_minutes = int(access_token_exp_minutes or 60)
        self._refresh_days = int(refresh_token_exp_days or 7)
        self._issuer = issuer
        self._audience = audience

    # ---------- Fábricas úteis ----------

    @classmethod
    def from_settings(cls) -> "JWTService":
        """
        Tenta construir o service a partir do AppSettings, se existir.
        Se não existir, cai em defaults seguros.
        """
        defaults = {
            "secret_key": "change-me-in-prod",
            "algorithm": "HS256",
            "access_token_exp_minutes": 60,
            "refresh_token_exp_days": 7,
            "issuer": None,
            "audience": None,
        }

        if AppSettings is None:
            return cls(**defaults)

        try:
            settings = AppSettings()  # type: ignore
            auth = getattr(settings, "auth", None)
            app = getattr(settings, "app", None)

            secret = (
                getattr(auth, "secret_key", None)
                or getattr(app, "secret_key", None)
                or defaults["secret_key"]
            )
            algorithm = (
                getattr(auth, "algorithm", None)
                or getattr(app, "algorithm", None)
                or defaults["algorithm"]
            )
            access_minutes = int(
                getattr(auth, "access_token_exp_minutes", None)
                or getattr(app, "access_token_exp_minutes", None)
                or defaults["access_token_exp_minutes"]
            )
            refresh_days = int(
                getattr(auth, "refresh_token_exp_days", None)
                or getattr(app, "refresh_token_exp_days", None)
                or defaults["refresh_token_exp_days"]
            )
            issuer = (
                getattr(auth, "issuer", None)
                or getattr(app, "issuer", None)
                or defaults["issuer"]
            )
            audience = (
                getattr(auth, "audience", None)
                or getattr(app, "audience", None)
                or defaults["audience"]
            )

            return cls(
                secret_key=secret,
                algorithm=algorithm,
                access_token_exp_minutes=access_minutes,
                refresh_token_exp_days=refresh_days,
                issuer=issuer,
                audience=audience,
            )
        except Exception:
            # Se algo falhar, volte para defaults (útil em dev)
            return cls(**defaults)

    # ---------- Criação de tokens ----------

    def generate_access_token(
        self,
        *,
        sub: str,
        email: Optional[str] = None,
        roles: Optional[List[str]] = None,
        extra_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Gera um access token curto (minutos).
        Claims padrão: sub, type="access", iat, nbf, exp, jti, (email, roles se informados), (iss/aud se configurados).
        """
        now = _utcnow()
        exp = now + timedelta(minutes=self._access_minutes)

        payload: Dict[str, Any] = {
            "sub": sub,
            "type": "access",
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "jti": str(uuid.uuid4()),
        }
        if email:
            payload["email"] = email
        if roles:
            payload["roles"] = roles
        if self._issuer:
            payload["iss"] = self._issuer
        if self._audience:
            payload["aud"] = self._audience
        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self._secret, algorithm=self._alg)

    def generate_refresh_token(
        self,
        *,
        sub: str,
        extra_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Gera um refresh token longo (dias). NÃO coloca email/roles (opcional), pois não é necessário.
        """
        now = _utcnow()
        exp = now + timedelta(days=self._refresh_days)

        payload: Dict[str, Any] = {
            "sub": sub,
            "type": "refresh",
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "jti": str(uuid.uuid4()),
        }
        if self._issuer:
            payload["iss"] = self._issuer
        if self._audience:
            payload["aud"] = self._audience
        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self._secret, algorithm=self._alg)

    # ---------- Verificação/decodificação ----------

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodifica e retorna as claims **sem** forçar audience/issuer (a menos que estejam configurados).
        Levanta JWTError em caso de falha.
        """
        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_iat": True,
            "verify_nbf": True,
        }
        kwargs: Dict[str, Any] = {
            "key": self._secret,
            "algorithms": [self._alg],
            "options": options,
        }
        if self._audience:
            kwargs["audience"] = self._audience
        if self._issuer:
            kwargs["issuer"] = self._issuer

        return jwt.decode(token, **kwargs)  # type: ignore[arg-type]

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica se é um token do tipo access.
        """
        try:
            payload = self.decode_token(token)
            if payload.get("type") != "access":
                raise JWTError("Tipo de token inválido (esperado 'access').")
            return payload
        except JWTError:
            raise
        except Exception as e:
            raise JWTError(str(e))

    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica se é um token do tipo refresh.
        """
        try:
            payload = self.decode_token(token)
            if payload.get("type") != "refresh":
                raise JWTError("Tipo de token inválido (esperado 'refresh').")
            return payload
        except JWTError:
            raise
        except Exception as e:
            raise JWTError(str(e))
