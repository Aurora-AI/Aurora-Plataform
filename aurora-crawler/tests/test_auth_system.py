"""Testes para sistema de autenticação"""

import pytest

from fastapi.testclient import TestClient
from aurora_platform.main import app
from fastapi import FastAPI


@pytest.fixture
def client():
    """Fixture para cliente de teste com estado inicializado"""
    test_client = TestClient(app)
    real_app = test_client.app
    # Desce até encontrar o FastAPI real
    while hasattr(real_app, "app") and not isinstance(real_app, FastAPI):
        next_app = getattr(real_app, "app", None)
        if next_app is None:
            break
        real_app = next_app
    if isinstance(real_app, FastAPI):
        if not hasattr(real_app.state, "kb_service"):
            from aurora_platform.services.knowledge_service import KnowledgeBaseService

            real_app.state.kb_service = KnowledgeBaseService()
    return test_client


def test_auth_router_included():
    """Testa se o router de auth foi incluído"""
    routes = [
        getattr(route, "path", "") for route in app.routes if hasattr(route, "path")
    ]
    auth_routes = [r for r in routes if r.startswith("/api/v1/auth")]
    assert len(auth_routes) > 0


def test_etp_router_included():
    """Testa se o router ETP foi incluído"""
    routes = [
        getattr(route, "path", "") for route in app.routes if hasattr(route, "path")
    ]
    etp_routes = [r for r in routes if r.startswith("/api/v1/etp")]
    assert len(etp_routes) > 0


def test_token_endpoint_exists(client):
    """Testa se endpoint de token existe"""
    response = client.post(
        "/api/v1/auth/token", data={"username": "wrong", "password": "wrong"}
    )
    # Deve retornar 401, não 404 (endpoint existe)
    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    """Testa endpoint protegido sem token"""
    response = client.post("/api/v1/etp/generate")
    assert response.status_code == 401
