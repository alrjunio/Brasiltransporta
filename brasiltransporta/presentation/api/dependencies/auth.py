# brasiltransporta/presentation/api/dependencies/auth.py
from __future__ import annotations
from typing import Any, Dict, Optional
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError  # ✅ usa python-jose

security = HTTPBearer(auto_error=True)

# ----------------- Helpers de ambiente -----------------
def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    return v if (v is not None and str(v).strip() != "") else default


# ----------------- Função principal -----------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    - Lê e valida o token Bearer JWT.
    - Usa o segredo configurado em JWT_SECRET ou SECRET_KEY.
    - Retorna um dicionário com os campos mínimos esperados pelo sistema.
    """
    token = (credentials.credentials or "").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")

    secret = _env("JWT_SECRET") or _env("SECRET_KEY")
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Configuração ausente: defina JWT_SECRET ou SECRET_KEY."
        )

    algorithms = [_env("JWT_ALGORITHM", "HS256")]
    issuer = _env("JWT_ISSUER")
    audience = _env("JWT_AUDIENCE")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=algorithms,
            issuer=issuer,
            audience=audience,
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    # Verifica se é token de acesso
    typ = payload.get("type") or payload.get("typ")
    if typ and str(typ).lower() != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Use um token de acesso")

    # Normaliza roles
    roles = payload.get("roles") or []
    if not isinstance(roles, (list, tuple, set)):
        roles = [roles] if roles else []

    # Retorna dict usado por authz.require_roles(...)
    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "roles": [str(r).lower() for r in roles],
        "jti": payload.get("jti"),
        "type": typ or "access",
    }
