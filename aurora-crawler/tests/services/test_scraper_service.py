import pytest
from unittest.mock import MagicMock, AsyncMock

from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2


@pytest.fixture
def mock_knowledge_base_service():
    """Mock do serviço de base de conhecimento."""
    mock = MagicMock()
    mock.add_document = MagicMock()
    return mock


@pytest.mark.asyncio
async def test_deep_dive_scrape_success(mock_knowledge_base_service):
    """
    Testa o fluxo de sucesso do scraping, garantindo que a ingestão é chamada.
    """
    # Arrange
    url = "http://example.com"
    scraper = DeepDiveScraperServiceV2()
    # Mock do método público
    scraper.fetch_page = AsyncMock(
        return_value="<html><body><p>Conteúdo de teste</p></body></html>"
    )
    await scraper.deep_dive_scrape(url)
    mock_knowledge_base_service.add_document.assert_called()


# Adicionar mais testes para casos de falha (ex: URL inválida, página sem conteúdo)
