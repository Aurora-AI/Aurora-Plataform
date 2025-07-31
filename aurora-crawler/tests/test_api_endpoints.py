"""Testes para endpoints da API"""

import pytest
from fastapi.testclient import TestClient
from aurora_platform.main import app


@pytest.fixture
def client():
    """Fixture para cliente de teste"""
    return TestClient(app)


def test_app_creation():
    """Testa criação da aplicação"""
    assert app is not None
    assert app.title == "Aurora Platform"


def test_knowledge_router_included():
    """Testa se o router de conhecimento foi incluído"""
    routes = [
        getattr(route, "path", "") for route in app.routes if hasattr(route, "path")
    ]
    knowledge_routes = [r for r in routes if r.startswith("/api/v1/knowledge")]
    assert len(knowledge_routes) > 0


def test_audio_router_included():
    """Testa se o router de áudio foi incluído"""
    routes = [
        getattr(route, "path", "") for route in app.routes if hasattr(route, "path")
    ]
    audio_routes = [r for r in routes if r.startswith("/api/v1/audio")]
    assert len(audio_routes) > 0


def test_document_router_included():
    """Testa se o router de documentos foi incluído"""
    routes = [
        getattr(route, "path", "") for route in app.routes if hasattr(route, "path")
    ]
    document_routes = [r for r in routes if r.startswith("/api/v1/documents")]
    assert len(document_routes) > 0
