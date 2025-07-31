import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, Response
from fastapi import HTTPException

# --- CORREÇÃO: Importando o nome correto da classe 'CnpjService' ---
from aurora_platform.services.cnpj_service import CnpjService

MOCK_CNPJ_VALIDO = "00000000000191"
MOCK_API_RESPONSE = {"razao_social": "EMPRESA TESTE LTDA"}


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_cnpj_data_sucesso(mock_get):
    """
    Testa o caso de sucesso da busca de dados de CNPJ.
    """
    # Arrange
    mock_get.return_value = Response(200, json=MOCK_API_RESPONSE)
    service = CnpjService()

    # Act
    result = await service.get_cnpj_data(MOCK_CNPJ_VALIDO)

    # Assert
    assert result == MOCK_API_RESPONSE
    mock_get.assert_called_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_get_cnpj_data_nao_encontrado(mock_get):
    """
    Testa o caso onde o CNPJ não é encontrado (HTTP 404).
    """
    # Arrange
    mock_get.return_value = Response(404)
    service = CnpjService()

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await service.get_cnpj_data("00000000000000")

    assert excinfo.value.status_code == 404
