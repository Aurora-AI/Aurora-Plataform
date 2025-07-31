import requests

BASE_URL = "http://127.0.0.1:8001"


def check_server():
    """Verifica se servidor está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Servidor OK: {response.json()}")
        assert True
    except:
        print("❌ Servidor não está rodando")
        assert False


def check_endpoints():
    """Verifica endpoints disponíveis"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ Docs disponível: {response.status_code}")
    except:
        print("❌ Docs não disponível")


if __name__ == "__main__":
    check_server()
    check_endpoints()
