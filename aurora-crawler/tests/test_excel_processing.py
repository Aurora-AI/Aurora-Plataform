import pytest
from src.aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService
from typing import Sequence, Dict


def test_excel_processing_valid_file():
    kb_mock = KnowledgeBaseService()
    processor = DocumentProcessingService(kb_mock)
    result = processor.extract_text_from_excel("valid_data.xlsx")
    assert isinstance(result, Sequence)
    assert len(result) > 0
    assert "Product" in result[0]


def test_excel_processing_invalid_file():
    kb_mock = KnowledgeBaseService()
    processor = DocumentProcessingService(kb_mock)
    with pytest.raises(ValueError):
        processor.extract_text_from_excel("corrupted.xlsx")
