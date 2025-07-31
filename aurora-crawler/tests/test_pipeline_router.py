import pytest
from fastapi.testclient import TestClient
from aurora_platform.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_pipeline_summarize_url(client):
    payload = {
        "project_name": "test_project",
        "sources": [{"source_type": "url", "source_path": "https://example.com"}],
        "actions": ["summarize_url"],
    }
    response = client.post("/api/v1/pipelines/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert any("summarize_url_result" in r for r in data["results"])


def test_pipeline_semantic_analysis(client, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Este é um documento de teste com conteúdo útil.")
    payload = {
        "project_name": "test_project",
        "sources": [{"source_type": "file", "source_path": str(test_file)}],
        "actions": ["semantic_analysis"],
    }
    response = client.post("/api/v1/pipelines/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert any("semantic_analysis_result" in r for r in data["results"])
