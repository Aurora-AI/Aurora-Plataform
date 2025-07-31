import requests
import json

# Configuração
BASE_URL = "http://localhost:8001/api/v1/knowledge"


def test_ingest():
    """Testa ingestão de documento"""
    url = f"{BASE_URL}/ingestions"
    payload = {
        "source_type": "url",
        "source_path": "https://www.alura.com.br/formacao-android-ia-google-ml-kit",
    }
    from requests.auth import HTTPBasicAuth

    print("🔄 Testando ingestão semântica (com autenticação)...")
    response = requests.post(
        url, json=payload, auth=HTTPBasicAuth("winhaski@live.com", "C@08$19&80i")
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 202


def test_search():
    """Testa busca na base de conhecimento"""
    url = f"{BASE_URL}/search"

    payload = {"query": "test document", "n_results": 3}

    print("\n🔍 Testando busca...")
    response = requests.post(url, json=payload)

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    assert response.status_code == 200


if __name__ == "__main__":
    print("🚀 Iniciando testes da API Aurora Platform\n")
    test_ingest()
    test_search()
    print(f"\n📊 Resultados: Todos os testes passaram com sucesso.")
