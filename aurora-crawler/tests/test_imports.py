"""Testes de importação dos módulos principais"""

import pytest


def test_knowledge_service_import():
    """Testa importação do KnowledgeBaseService"""
    from aurora_platform.services.knowledge_service import KnowledgeBaseService

    assert KnowledgeBaseService is not None


def test_semantic_analysis_import():
    """Testa importação do SemanticAnalysisService"""
    from aurora_platform.services.semantic_analysis_service import (
        SemanticAnalysisService,
    )

    assert SemanticAnalysisService is not None


def test_scraper_service_import():
    """Testa importação do DeepDiveScraperServiceV2"""
    from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2

    assert DeepDiveScraperServiceV2 is not None


def test_audio_service_import():
    """Testa importação do AudioTranscriptionService"""
    from aurora_platform.services.audio_transcription_service import (
        AudioTranscriptionService,
    )

    assert AudioTranscriptionService is not None


def test_document_service_import():
    """Testa importação do DocumentProcessingService"""
    from aurora_platform.services.document_processing_service import (
        DocumentProcessingService,
    )

    assert DocumentProcessingService is not None


def test_main_app_import():
    """Testa importação da aplicação principal"""
    from aurora_platform.main import app

    assert app is not None
