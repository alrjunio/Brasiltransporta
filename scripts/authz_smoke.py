# scripts/authz_smoke.py
from __future__ import annotations

import json
import os
import sys
from typing import Optional, Tuple

import requests


BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def post_json(path: str, payload: dict, timeout: int = 5) -> requests.Response:
    url = f"{BASE}{path}"
    return requests.post(url, json=payload, timeout=timeout)


def get_auth(path: str, token: str, timeout: int = 5) -> requests.Response:
    url = f"{BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=timeout)


def ensure_user(email: str, password: str, roles: Optional[list[str]] = None, full_name: str = "") -> None:
    payload = {"email": email, "password": password}
    if full_name:
        payload["full_name"] = full_name
    if roles:
        payload["roles"] = roles  # funciona se seu /auth/register já aceitar roles
    r = post_json("/auth/register", payload)
    # 200/201: criado; 400/409: já existe → ok
    if r.status_code >= 500:
        print(f"[ERRO] /auth/register {email}: {r.status_code} {r.text}", file=sys.stderr)
        sys.exit(1)


def login(email: str, password: str) -> str:
    r = post_json("/auth/login", {"email": email, "password": password})
    if r.status_code != 200:
        print(f"[ERRO] /auth/login {email}: {r.status_code} {r.text}", file=sys.stderr)
        sys.exit(1)
    data = r.json()
    return data["access_token"]


def check_endpoint(name: str, path: str, token: str, expected_status: int) -> Tuple[bool, int, str]:
    r = get_auth(path, token)
    ok = r.status_code == expected_status
    msg = ""
    try:
        msg = json.dumps(r.json())
    except Exception:
        msg = r.text[:200]
    print(f"- {name:<26} -> esperado {expected_status}, obtido {r.status_code} | {msg}")
    return ok, r.status_code, msg


def main() -> int:
    print(f"== AuthZ Smoke = {BASE} ==")

    # 1) Garantir BUYER
    buyer_email = os.getenv("BUYER_EMAIL", "teste@login.com")
    buyer_pass = os.getenv("BUYER_PASS", "Senha123!")
    ensure_user(buyer_email, buyer_pass, roles=["buyer"], full_name="Buyer Teste")
    buyer_token = login(buyer_email, buyer_pass)

    # 2) Garantir ADMIN
    admin_email = os.getenv("ADMIN_EMAIL", "admin@login.com")
    admin_pass = os.getenv("ADMIN_PASS", "Senha123!")
    # Se seu /auth/register NÃO aceitar roles, crie como buyer e depois promova por SQL fora deste script.
    ensure_user(admin_email, admin_pass, roles=["admin"], full_name="Admin Teste")
    admin_token = login(admin_email, admin_pass)

    print("\n[BUYER] Testando /auth/*-ping")
    b1 = check_endpoint("buyer-ping (buyer)", "/auth/buyer-ping", buyer_token, 200)
    b2 = check_endpoint("seller-ping (buyer)", "/auth/seller-ping", buyer_token, 403)
    b3 = check_endpoint("admin-ping (buyer)", "/auth/admin-ping", buyer_token, 403)

    print("\n[ADMIN] Testando /auth/*-ping")
    a1 = check_endpoint("buyer-ping (admin)", "/auth/buyer-ping", admin_token, 200)
    a2 = check_endpoint("seller-ping (admin)", "/auth/seller-ping", admin_token, 200)
    a3 = check_endpoint("admin-ping (admin)", "/auth/admin-ping", admin_token, 200)

    all_ok = all(x[0] for x in (b1, b2, b3, a1, a2, a3))
    print("\nResultado geral:", "OK ✅" if all_ok else "FALHOU ❌")
    return 0 if all_ok else 2


if __name__ == "__main__":
    sys.exit(main())
