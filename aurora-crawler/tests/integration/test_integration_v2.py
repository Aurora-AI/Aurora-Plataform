import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"


def test_ingest_web():
    """ÉPICO 2: Teste de ingestão web"""
    print("🔄 ÉPICO 2: Testando ingestão web...")

    url = f"{BASE_URL}/api/v1/knowledge/ingestions"
    payload = {
        "source_type": "url",
        "source_path": "https://www.alura.com.br/formacao-android-ia-google-ml-kit",
    }
    from requests.auth import HTTPBasicAuth

    try:
        response = requests.post(
            url,
            json=payload,
            auth=HTTPBasicAuth("winhaski@live.com", "C@08$19&80i"),
            timeout=60,
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert (
            response.status_code == 202
        ), f"Ingestão web não retornou 202, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na ingestão: {e}")
        assert False, f"Erro na ingestão web: {e}"


def test_ask():
    """ÉPICO 3: Teste de consulta RAG"""
    print("\n🔄 ÉPICO 3: Testando consulta RAG...")

    url = f"{BASE_URL}/api/v1/knowledge/ask"
    payload = {"query": "What is FastAPI?", "n_results": 3}

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Question: {result.get('question')}")
        print(f"Answer: {result.get('answer', '')[:100]}...")
        print(f"Sources: {result.get('sources')}")
        assert (
            response.status_code == 200
        ), f"Consulta RAG não retornou 200, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
        assert False, f"Erro na consulta RAG: {e}"


def test_etp_generator():
    """ÉPICO 4: Teste do gerador ETP"""
    print("\n🔄 ÉPICO 4: Testando ETP Generator...")

    url = f"{BASE_URL}/api/v1/etp/generate"
    payload = {
        "topic": "FastAPI",
        "sections": ["Introdução", "Características", "Conclusão"],
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"ETP Title: {result.get('etp', {}).get('title')}")
        print(f"Knowledge Sources: {result.get('etp', {}).get('knowledge_sources')}")
        assert (
            response.status_code == 200
        ), f"ETP Generator não retornou 200, retornou {response.status_code}"
    except Exception as e:
        print(f"❌ Erro no ETP: {e}")
        assert False, f"Erro no ETP Generator: {e}"


def main():
    print("🚀 TESTE DE INTEGRAÇÃO V2 - ENDPOINTS CORRIGIDOS\n")

    time.sleep(2)

    results = {
        "ingest": test_ingest_web(),
        "ask": test_ask(),
        "etp": test_etp_generator(),
    }

    print(f"\n📊 RELATÓRIO FINAL:")
    print(f"✅ Ingestão Web: {'PASSOU' if results['ingest'] else '❌ FALHOU'}")
    print(f"✅ Consulta RAG: {'PASSOU' if results['ask'] else '❌ FALHOU'}")
    print(f"✅ ETP Generator: {'PASSOU' if results['etp'] else '❌ FALHOU'}")

    # Garante que todos os valores são booleanos para evitar erro de tipo
    bools = [bool(v) for v in results.values()]
    success_rate = sum(bools) / len(bools) * 100
    print(f"\n🎯 Taxa de Sucesso: {success_rate:.1f}%")


if __name__ == "__main__":
    main()
