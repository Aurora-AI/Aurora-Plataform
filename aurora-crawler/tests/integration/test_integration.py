import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"


def test_ingest():
    """ÉPICO 2: Teste de ingestão"""
    print("🔄 ÉPICO 2: Testando ingestão...")

    url = f"{BASE_URL}/api/v1/knowledge/ingestions"
    payload = {"source_type": "url", "source_path": "https://fastapi.tiangolo.com/"}
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert (
            response.status_code == 202
        ), f"Ingestão não retornou 202, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na ingestão: {e}")
        assert False, f"Erro na ingestão: {e}"


def test_search():
    """ÉPICO 3: Teste de consulta RAG"""
    print("\n🔄 ÉPICO 3: Testando consulta...")

    url = f"{BASE_URL}/api/v1/knowledge/search"
    payload = {"query": "What is FastAPI?", "n_results": 3}

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        # results é uma lista de documentos
        results_list = result.get("results", [])
        print(f"Results found: {len(results_list)}")
        assert (
            response.status_code == 200
        ), f"Consulta não retornou 200, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
        assert False, f"Erro na consulta: {e}"


def test_etp():
    """ÉPICO 4: Teste do gerador ETP"""
    print("\n🔄 ÉPICO 4: Testando ETP Generator...")

    url = f"{BASE_URL}/api/v1/etp/generate"
    payload = {"topic": "Teste de API"}
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code in [
            200,
            401,
        ], f"ETP não retornou 200 ou 401, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro no ETP: {e}")
        assert False, f"Erro no ETP: {e}"


def main():
    print("🚀 INICIANDO TESTE DE INTEGRAÇÃO COMPLETO\n")

    # Aguardar servidor estar pronto
    print("⏳ Aguardando servidor...")
    time.sleep(2)

    results = {"ingest": test_ingest(), "search": test_search(), "etp": test_etp()}

    print(f"\n📊 RELATÓRIO FINAL:")
    print(f"✅ Ingestão: {'PASSOU' if results['ingest'] else '❌ FALHOU'}")
    print(f"✅ Consulta: {'PASSOU' if results['search'] else '❌ FALHOU'}")
    print(f"✅ ETP: {'PASSOU' if results['etp'] else '❌ FALHOU'}")

    # Garante que todos os valores são booleanos para evitar erro de tipo
    bools = [bool(v) for v in results.values()]
    success_rate = sum(bools) / len(bools) * 100
    print(f"\n🎯 Taxa de Sucesso: {success_rate:.1f}%")


if __name__ == "__main__":
    main()
