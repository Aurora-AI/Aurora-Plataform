"""Testes para SemanticAnalysisService"""

import pytest
from aurora_platform.services.semantic_analysis_service import SemanticAnalysisService


def test_semantic_service_init():
    """Testa inicialização do serviço"""
    service = SemanticAnalysisService()
    assert service is not None


def test_is_document_coherent():
    """Testa verificação de coerência"""
    service = SemanticAnalysisService()

    # Texto coerente
    coherent_text = (
        "Este é um documento com conteúdo útil e informativo sobre tecnologia."
    )
    assert service.is_document_coherent(coherent_text) == True

    # Texto muito curto
    short_text = "abc"
    assert service.is_document_coherent(short_text) == False

    # Texto vazio
    assert service.is_document_coherent("") == False


def test_semantic_chunking(sample_text):
    """Testa fragmentação semântica"""
    service = SemanticAnalysisService()
    chunks = service.semantic_chunking(sample_text)
    assert isinstance(chunks, list)
    assert len(chunks) > 0

    # Teste com texto longo
    long_text = sample_text * 100
    chunks = service.semantic_chunking(long_text, max_chunk_size=500)
    assert len(chunks) > 1
