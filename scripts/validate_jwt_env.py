# scripts/validate_jwt_env.py
"""
Script de diagnóstico de JWT e ambiente.
Mostra:
  - Variáveis JWT_* e SECRET_KEY ativas no container.
  - Header e payload do token (sem verificar assinatura).
  - Teste de validação com o segredo e algoritmo atuais.
"""

import os
import sys
import requests
from jose import jwt, JWTError

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")
EMAIL = os.getenv("TEST_EMAIL", "teste@login.com")
PASSWORD = os.getenv("TEST_PASSWORD", "Senha123!")

print("=" * 80)
print("🚀 Validação do ambiente JWT e token".center(80))
print("=" * 80)

# ----------------------------------------------------------------------
# 1) Variáveis de ambiente relevantes
print("\n🔍 Variáveis JWT e SECRET_KEY no ambiente:\n")
for key in sorted(os.environ.keys()):
    if key.startswith("JWT_") or key.startswith("SECRET_KEY"):
        print(f"{key} = {os.environ[key]}")

# ----------------------------------------------------------------------
# 2) Solicita token de login
print("\n📨 Gerando token via /auth/login...\n")
try:
    response = requests.post(
        f"{BASE}/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    token = data.get("access_token")
    if not token:
        print("❌ Nenhum token retornado!")
        sys.exit(1)
    print(f"✅ Token recebido (primeiros 60 chars): {token[:60]}...")
except Exception as e:
    print(f"❌ Erro ao obter token: {e}")
    sys.exit(1)

# ----------------------------------------------------------------------
# 3) Inspeciona header e payload SEM validação
print("\n📋 Decodificando header e payload (sem verificar assinatura):\n")
try:
    header = jwt.get_unverified_header(token)
    payload = jwt.get_unverified_claims(token)
    print("== HEADER ==")
    for k, v in header.items():
        print(f"  {k}: {v}")
    print("\n== PAYLOAD ==")
    for k, v in payload.items():
        print(f"  {k}: {v}")
except Exception as e:
    print(f"❌ Erro ao inspecionar token: {e}")
    sys.exit(1)

# ----------------------------------------------------------------------
# 4) Validação completa com as variáveis do ambiente
print("\n🔐 Tentando validar token com as configs do ambiente:\n")
secret = os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY")
algorithm = os.getenv("JWT_ALGORITHM", "HS256")
issuer = os.getenv("JWT_ISSUER")
audience = os.getenv("JWT_AUDIENCE")

print(f"Usando SECRET: {'(definido)' if secret else '(ausente)'}")
print(f"Algoritmo: {algorithm}")
print(f"Issuer esperado: {issuer}")
print(f"Audience esperado: {audience}")
print("-" * 60)

if not secret:
    print("❌ Nenhum segredo definido em JWT_SECRET ou SECRET_KEY.")
    sys.exit(1)

try:
    payload_verified = jwt.decode(
        token,
        secret,
        algorithms=[algorithm],
        issuer=issuer,
        audience=audience,
    )
    print("✅ Token validado com sucesso!\n")
    for k, v in payload_verified.items():
        print(f"  {k}: {v}")
except JWTError as e:
    print(f"❌ Token inválido: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

print("\n📘 Interprete os resultados:")
print("  - Se o alg no header ≠ JWT_ALGORITHM → alinhe as duas configs.")
print("  - Se o token tem iss/aud → defina JWT_ISSUER/AUDIENCE iguais.")
print("  - Se deu JWTError → verifique se o login e validador usam a mesma chave e algoritmo.")
print("=" * 80)
