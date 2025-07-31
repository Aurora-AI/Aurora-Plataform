import requests
import json

BASE_URL = "http://localhost:8001/api/v1/knowledge/ask"


def test_rag_alura_relevant():
    """Testa se o RAG responde corretamente com conteúdo relevante da Alura."""
    payload = {
        "query": "Quais os pré requisitos para criar um app com inteligência Artificial embarcada?",
        "n_results": 5,
    }
    response = requests.post(BASE_URL, json=payload)
    print("\n[ALURA RAG] Status:", response.status_code)
    print(
        "[ALURA RAG] Response:",
        json.dumps(response.json(), indent=2, ensure_ascii=False),
    )
    assert response.status_code == 200
    answer = response.json().get("answer", "").lower()
    # Espera-se que a resposta mencione termos como "android", "ml kit", "google", "pré-requisito"
    assert any(
        term in answer
        for term in [
            "android",
            "ml kit",
            "google",
            "pré-requisito",
            "inteligência artificial",
        ]
    ), "Resposta não parece relevante ao conteúdo da Alura."


def test_rag_aurora_sem_conteudo():
    """Testa se o RAG responde honestamente quando não há conteúdo relevante."""
    payload = {
        "query": "Usando o seu conhecimento sobre o projeto Aurora, nosso projeto proprietário, e com base no conhecimento adquirido da Alura, quais são os passos lógicos para migrar a Aurora de um software web para um software mobile?",
        "n_results": 5,
    }
    response = requests.post(BASE_URL, json=payload)
    print("\n[AURORA RAG] Status:", response.status_code)
    print(
        "[AURORA RAG] Response:",
        json.dumps(response.json(), indent=2, ensure_ascii=False),
    )
    assert response.status_code == 200
    answer = response.json().get("answer", "").lower()
    # Espera-se que a resposta seja honesta sobre não ter contexto suficiente
    assert any(
        term in answer
        for term in [
            "não encontrei informações",
            "não contém dados suficientes",
            "limitação do conhecimento",
            "não foi possível",
        ]
    ), "Resposta não foi honesta sobre ausência de contexto."
