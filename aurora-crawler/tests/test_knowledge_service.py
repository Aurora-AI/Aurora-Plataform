"""Testes para KnowledgeBaseService"""

import pytest
import tempfile
import shutil
from aurora_platform.services.knowledge_service import KnowledgeBaseService


@pytest.fixture
def temp_db():
    """Fixture para banco temporário"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_knowledge_service_init():
    """Testa inicialização do serviço"""
    kb = KnowledgeBaseService()
    assert kb.client is not None


def test_add_document():
    """Testa adição de documento"""
    kb = KnowledgeBaseService()
    kb.ingest_document(
        document_id="test_doc",
        text="Este é um texto de exemplo",
        metadata={"source": "test"},
        collection_name="test_collection",
    )
    # Se não lançar exceção, passou


def test_retrieve_document():
    """Testa busca de documento"""
    kb = KnowledgeBaseService()
    kb.ingest_document(
        document_id="test_doc",
        text="Este é um texto de exemplo",
        metadata={"source": "test"},
        collection_name="test_collection",
    )
    results = kb.query_collection(
        query="exemplo", collection_name="test_collection", n_results=1
    )
    assert results is not None
