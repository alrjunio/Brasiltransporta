# brasiltransporta/presentation/api/dependencies/authz.py
from __future__ import annotations
from typing import Iterable, Callable, Set, Any, Dict, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os
from jose import jwt, JWTError  # ✅ usa python-jose

# ----------------- Helpers de ambiente / JWT fallback -----------------
def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    return v if (v is not None and str(v).strip() != "") else default

_security = HTTPBearer(auto_error=True)


def _verify_with_jose(token: str) -> Dict[str, Any]:
    """
    Valida token JWT usando python-jose (HS256 por padrão).
    Requer JWT_SECRET (ou SECRET_KEY) no ambiente.
    """
    secret = _env("JWT_SECRET") or _env("SECRET_KEY")
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Config ausente: defina JWT_SECRET (ou SECRET_KEY) para validar tokens."
        )

    algorithms = [_env("JWT_ALGORITHM", "HS256")]
    issuer = _env("JWT_ISSUER")
    audience = _env("JWT_AUDIENCE")
    leeway = int(_env("JWT_LEEWAY_SECONDS", "0"))

    options = {
        "verify_signature": True,
        "verify_aud": bool(audience),
        "verify_iss": bool(issuer),
    }

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=algorithms,
            issuer=issuer,
            audience=audience,
            options=options,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Falha ao validar token: {str(e)}"
        )
    return payload


# Tenta importar get_current_user “oficial”, senão usa fallback interno
try:
    from brasiltransporta.presentation.api.dependencies.auth import get_current_user  # type: ignore
except Exception:
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_security)) -> Dict[str, Any]:
        token = (credentials.credentials or "").strip()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")

        payload = _verify_with_jose(token)

        typ = payload.get("type") or payload.get("typ")
        if typ and str(typ).lower() != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Use um token de acesso")

        roles = payload.get("roles") or []
        if not isinstance(roles, (list, tuple, set)):
            roles = [roles] if roles else []

        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "roles": [str(r).lower() for r in roles],
            "jti": payload.get("jti"),
            "type": typ or "access",
        }


# ----------------- Guard de autorização -----------------
def _normalize_roles(values: Iterable[str] | None) -> Set[str]:
    if not values:
        return set()
    return {str(v).strip().lower() for v in values}


def require_roles(*required_roles: str) -> Callable:
    """
    Guard de autorização baseado em roles.
    Basta o usuário ter uma das roles exigidas.
    Admin tem acesso total.
    """
    if not required_roles:
        raise ValueError("require_roles(...): forneça pelo menos uma role requerida.")
    required = _normalize_roles(required_roles)

    async def _dep(current_user=Depends(get_current_user)):
        roles = None
        if hasattr(current_user, "roles"):
            roles = getattr(current_user, "roles")
        elif isinstance(current_user, dict):
            roles = current_user.get("roles")
        user_roles = _normalize_roles(roles)

        if "admin" in user_roles:
            return current_user
        if user_roles.intersection(required):
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente",
        )

    return _dep
