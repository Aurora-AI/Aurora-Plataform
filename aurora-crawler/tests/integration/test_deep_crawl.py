import requests
import time

BASE_URL = "http://127.0.0.1:8001"


def test_deep_crawl_endpoint():
    """Testa o novo endpoint de deep crawl"""
    print("🔄 Testando deep crawl /ingest-deep-crawl-from-url...")

    url = f"{BASE_URL}/api/v1/pipelines/ingest-deep-crawl-from-url"
    payload = {"url": "https://redelog.rj.gov.br/redelog/"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert (
            response.status_code == 202
        ), f"Deep crawl não retornou 202, retornou {response.status_code}"
        print("✅ Deep crawl iniciado em background!")
        print("⏳ Aguardando processamento...")
        time.sleep(10)  # Aguarda processamento
    except Exception as e:
        print(f"❌ Erro no deep crawl: {e}")
        assert False, f"Erro no deep crawl: {e}"


def test_search_after_crawl():
    """Testa busca após deep crawl"""
    print("\n🔄 Testando busca após deep crawl...")

    url = f"{BASE_URL}/api/v1/knowledge/search"
    payload = {"query": "redelog", "n_results": 5}

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        results_count = len(result.get("results", []))
        print(f"Results: {results_count}")

        if results_count > 0:
            print(f"✅ Encontrou {results_count} resultados relacionados ao site!")
        assert (
            response.status_code == 200
        ), f"Busca após deep crawl não retornou 200, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        assert False, f"Erro na busca após deep crawl: {e}"


def test_regular_crawl_comparison():
    """Testa crawl regular para comparação"""
    print("\n🔄 Testando crawl regular para comparação...")

    url = f"{BASE_URL}/api/v1/pipelines/ingest-documents-from-url"
    payload = {"url": "https://fastapi.tiangolo.com/"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 202
    except Exception as e:
        print(f"❌ Erro no crawl regular: {e}")
        assert False


def main():
    print("🚀 TESTANDO DEEP CRAWL v2.1\n")

    # Teste deep crawl
    deep_crawl_ok = test_deep_crawl_endpoint()

    # Aguarda processamento
    if deep_crawl_ok:
        print("\n⏳ Aguardando conclusão do deep crawl...")
        time.sleep(15)

    # Teste busca
    search_ok = test_search_after_crawl()

    # Teste comparativo
    regular_ok = test_regular_crawl_comparison()

    print(f"\n📊 RESULTADO:")
    print(f"✅ Deep Crawl: {'PASSOU' if deep_crawl_ok else '❌ FALHOU'}")
    print(f"✅ Busca: {'PASSOU' if search_ok else '❌ FALHOU'}")
    print(f"✅ Crawl Regular: {'PASSOU' if regular_ok else '❌ FALHOU'}")

    # Garante que todos os valores são inteiros (0 ou 1) para evitar erro de tipo
    bools = [bool(deep_crawl_ok), bool(search_ok), bool(regular_ok)]
    success_rate = sum(bools) / 3 * 100
    print(f"\n🎯 Taxa de Sucesso: {success_rate:.1f}%")


if __name__ == "__main__":
    main()
