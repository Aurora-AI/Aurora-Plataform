import pytest
from unittest.mock import MagicMock, patch

from src.aurora_platform.services.knowledge_service import KnowledgeBaseService


@pytest.fixture
def mock_chromadb_collection():
    """Mock da coleção do ChromaDB para evitar I/O de disco."""
    mock_collection = MagicMock()
    return mock_collection


@patch("chromadb.PersistentClient")
def test_ingest_document_success(mock_persistent_client, mock_chromadb_collection):
    """
    Testa se o método de ingestão chama corretamente o 'add' da coleção ChromaDB.
    """
    # Arrange
    # Configura o mock do cliente para retornar nosso mock de coleção
    mock_persistent_client.return_value.get_or_create_collection.return_value = (
        mock_chromadb_collection
    )

    kb_service = KnowledgeBaseService(persist_directory="/fake/path")
    doc_id = "doc_test_1"
    text = "Texto do documento de teste."
    metadata = {"source": "test"}

    # Act
    kb_service.add_document(doc_id, text, metadata, collection_name="test_collection")

    # Assert
    mock_chromadb_collection.add.assert_called_once_with(
        ids=[doc_id], documents=[text], metadatas=[metadata]
    )


# Adicionar mais testes para outros métodos públicos (ex: busca)
