"""Testes para DeepDiveScraperServiceV2"""

import pytest
from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2


def test_scraper_service_init():
    """Testa inicialização do serviço"""
    service = DeepDiveScraperServiceV2()
    assert service is not None
    assert service.temp_dir is not None


def test_extract_text_from_pdf():
    """Testa extração de texto de PDF (método privado)"""
    service = DeepDiveScraperServiceV2()
    # Apenas verifica se o método existe
    assert hasattr(service, "_extract_text_from_pdf")
    assert callable(service._extract_text_from_pdf)


@pytest.mark.asyncio
async def test_download_pdfs_invalid_url():
    """Testa download com URL inválida"""
    service = DeepDiveScraperServiceV2()

    with pytest.raises(Exception):
        await service.download_pdfs_from_url("invalid-url")
