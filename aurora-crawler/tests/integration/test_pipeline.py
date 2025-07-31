import requests
import time

BASE_URL = "http://127.0.0.1:8001"


def test_pipeline_endpoint():
    """Testa o novo endpoint de pipeline"""
    print("🔄 Testando pipeline /ingest-documents-from-url...")

    url = f"{BASE_URL}/api/v1/pipelines/ingest-documents-from-url"
    payload = {"url": "https://pge.rj.gov.br/checklists-lei-1413321"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 202
        print("✅ Pipeline iniciado em background!")
        print("⏳ Aguardando processamento...")
        time.sleep(5)  # Aguarda um pouco para ver logs
    except Exception as e:
        print(f"❌ Erro no pipeline: {e}")
        assert False, f"Erro no pipeline: {e}"


def test_search_after_pipeline():
    """Testa busca após pipeline"""
    print("\n🔄 Testando busca após pipeline...")

    url = f"{BASE_URL}/api/v1/knowledge/search"
    payload = {"query": "checklist", "n_results": 3}

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Results: {len(result.get('results', []))}")
        assert response.status_code == 200
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        assert False, f"Erro na busca: {e}"


def main():
    print("🚀 TESTANDO PIPELINE DE INGESTÃO\n")
    test_pipeline_endpoint()
    print("\n⏳ Aguardando conclusão do pipeline...")
    time.sleep(10)
    test_search_after_pipeline()
    print(f"\n📊 RESULTADO: Testes executados via main()")


if __name__ == "__main__":
    main()
