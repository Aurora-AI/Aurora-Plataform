import pytest
from aurora_platform.services.knowledge_query_service import KnowledgeQueryService
from unittest.mock import MagicMock


@pytest.fixture
def mock_kb_service():
    kb_service = MagicMock()
    # Simula retorno do método retrieve
    kb_service.retrieve.return_value = [
        {
            "documents": ["Doc 1", "Doc 2"],
            "metadatas": [{"source": "ai.google.dev"}, {"source": "redelog"}],
        }
    ]
    return kb_service


@pytest.fixture
def query_service(mock_kb_service):
    return KnowledgeQueryService(mock_kb_service)


def test_answer_query_retorna_resposta_relevante(query_service):
    result = query_service.answer_query("gemini modelo", n_results=1)
    assert result["question"] == "gemini modelo"
    assert "Gemini" in result["answer"] or "Não encontrei" in result["answer"]
    assert isinstance(result["sources"], int)
    assert "chain_of_thought" in result


def test_answer_query_sem_contexto(query_service, mock_kb_service):
    # Simula retorno vazio
    mock_kb_service.retrieve.return_value = []
    result = query_service.answer_query("pergunta irrelevante", n_results=1)
    assert result["sources"] == 0
    assert "Não encontrei" in result["answer"]


def test_answer_query_tipo_incorreto(query_service):
    with pytest.raises(AssertionError):
        query_service.answer_query(123, n_results=1)
    with pytest.raises(AssertionError):
        query_service.answer_query("teste", n_results="um")
