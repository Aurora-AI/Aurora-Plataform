"""Testes para DocumentProcessingService"""

import pytest
import tempfile
import os
from aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)
from aurora_platform.services.knowledge_service import KnowledgeBaseService


@pytest.fixture
def kb_service():
    """Fixture para KnowledgeBaseService"""
    return KnowledgeBaseService()


def test_document_service_init(kb_service):
    """Testa inicialização do serviço"""
    service = DocumentProcessingService(kb_service)
    assert service is not None
    assert service.kb_service is not None


def test_process_and_ingest_files_empty_list(kb_service):
    """Testa processamento de lista vazia"""
    service = DocumentProcessingService(kb_service)
    result = service.process_and_ingest_files([], collection_name="test_collection")
    assert result == []


def test_process_and_ingest_files_unsupported_format(kb_service):
    """Testa arquivo com formato não suportado"""
    service = DocumentProcessingService(kb_service)

    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        f.write(b"test content")
        temp_path = f.name

    try:
        result = service.process_and_ingest_files(
            [temp_path], collection_name="test_collection"
        )
        assert result == []
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
