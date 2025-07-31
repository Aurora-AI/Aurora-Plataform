import pytest
import sys
import os
from pathlib import Path
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from aurora_platform.main import app
from aurora_platform.api.v1.endpoints import (
    knowledge_router,
    audio_router,
    document_router,
    auth_router,
    etp_router,
    pipeline_router,
)

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def session():
    """Fixture para banco de dados em memória isolado por teste."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    """Fixture para cliente de teste FastAPI com todos os roteadores registrados."""
    # Garante que todos os roteadores estão incluídos
    test_app = app
    test_app.include_router(
        knowledge_router.router, prefix="/api/v1/knowledge", tags=["knowledge"]
    )
    test_app.include_router(audio_router.router, prefix="/api/v1/audio", tags=["audio"])
    test_app.include_router(
        document_router.router, prefix="/api/v1/documents", tags=["documents"]
    )
    test_app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
    test_app.include_router(etp_router.router, prefix="/api/v1/etp", tags=["etp"])
    test_app.include_router(
        pipeline_router.router, prefix="/api/v1/pipelines", tags=["pipelines"]
    )
    return TestClient(test_app)


@pytest.fixture
def temp_file():
    """Fixture para criar arquivo temporário"""
    import tempfile

    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)


@pytest.fixture
def sample_text():
    """Fixture com texto de exemplo"""
    return "Este é um texto de exemplo para testes."
