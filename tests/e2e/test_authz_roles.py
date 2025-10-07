# tests/e2e/test_authz_roles.py
from __future__ import annotations

import os
import pytest
import requests

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def post_json(path: str, payload: dict, timeout: int = 5) -> requests.Response:
    url = f"{BASE}{path}"
    return requests.post(url, json=payload, timeout=timeout)


def get_auth(path: str, token: str, timeout: int = 5) -> requests.Response:
    url = f"{BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, timeout=timeout)


def ensure_user(email: str, password: str, roles=None, full_name: str = "") -> None:
    payload = {"email": email, "password": password}
    if full_name:
        payload["full_name"] = full_name
    if roles:
        payload["roles"] = roles
    r = post_json("/auth/register", payload)
    assert r.status_code in (200, 201, 400, 409), f"/auth/register falhou: {r.status_code} {r.text}"


def login(email: str, password: str) -> str:
    r = post_json("/auth/login", {"email": email, "password": password})
    assert r.status_code == 200, f"/auth/login falhou: {r.status_code} {r.text}"
    return r.json()["access_token"]


@pytest.mark.e2e
def test_authz_buyer_and_admin_pings():
    buyer_email = os.getenv("BUYER_EMAIL", "teste@login.com")
    buyer_pass = os.getenv("BUYER_PASS", "Senha123!")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@login.com")
    admin_pass = os.getenv("ADMIN_PASS", "Senha123!")

    # Garante usuários
    ensure_user(buyer_email, buyer_pass, roles=["buyer"], full_name="Buyer Teste")
    ensure_user(admin_email, admin_pass, roles=["admin"], full_name="Admin Teste")

    # Logins
    buyer_token = login(buyer_email, buyer_pass)
    admin_token = login(admin_email, admin_pass)

    # Buyer deve passar só no buyer-ping
    r = get_auth("/auth/buyer-ping", buyer_token)
    assert r.status_code == 200, r.text

    r = get_auth("/auth/seller-ping", buyer_token)
    assert r.status_code == 403, r.text

    r = get_auth("/auth/admin-ping", buyer_token)
    assert r.status_code == 403, r.text

    # Admin deve passar em todos
    for path in ("/auth/buyer-ping", "/auth/seller-ping", "/auth/admin-ping"):
        r = get_auth(path, admin_token)
        assert r.status_code == 200, f"{path} -> {r.status_code} {r.text}"
