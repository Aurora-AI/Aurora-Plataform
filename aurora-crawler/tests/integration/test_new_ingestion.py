import requests
import json

BASE_URL = "http://127.0.0.1:8001"


def test_new_ingestion_endpoint():
    """Testa o novo endpoint consolidado de ingestão"""
    print("🔄 Testando novo endpoint /ingestions...")

    url = f"{BASE_URL}/api/v1/knowledge/ingestions"
    payload = {"source_type": "url", "source_path": "https://fastapi.tiangolo.com/"}

    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert (
            response.status_code == 202
        ), f"Novo endpoint de ingestão não retornou 202, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na ingestão: {e}")
        assert False, f"Erro na ingestão: {e}"


def test_search_endpoint():
    """Testa o endpoint de busca refatorado"""
    print("\n🔄 Testando endpoint /search...")

    url = f"{BASE_URL}/api/v1/knowledge/search"
    payload = {"query": "What is FastAPI?", "n_results": 3}

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Results: {len(result.get('results', []))}")
        assert (
            response.status_code == 200
        ), f"Busca não retornou 200, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        assert False, f"Erro na busca: {e}"


def main():
    print("🚀 TESTANDO API REFATORADA\n")

    results = {
        "ingestion": test_new_ingestion_endpoint(),
        "search": test_search_endpoint(),
    }

    print(f"\n📊 RESULTADO:")
    print(f"✅ Ingestão: {'PASSOU' if results['ingestion'] else '❌ FALHOU'}")
    print(f"✅ Busca: {'PASSOU' if results['search'] else '❌ FALHOU'}")

    # Garante que todos os valores são booleanos para evitar erro de tipo
    bools = [bool(v) for v in results.values()]
    success_rate = sum(bools) / len(bools) * 100
    print(f"\n🎯 Taxa de Sucesso: {success_rate:.1f}%")


if __name__ == "__main__":
    main()
