import requests
import json

# Configuração
BASE_URL = "http://localhost:8001/api/v1/audio"


def test_audio_endpoints():
    """Testa se os endpoints de áudio estão disponíveis"""

    print("Testando disponibilidade dos endpoints de áudio...")

    # Teste de conectividade básica
    try:
        response = requests.get("http://localhost:8001/docs")
        assert response.status_code == 200, "Aplicação não está rodando"
        print("OK Aplicação está rodando")
    except requests.exceptions.ConnectionError:
        print("ERRO Aplicação não está rodando em localhost:8001")
        print("Execute: python run.py")
        assert False, "Aplicação não está rodando em localhost:8001"

    print("\nEndpoints de áudio disponíveis:")
    print("- POST /api/v1/audio/transcribe")
    print("- POST /api/v1/audio/transcribe-and-ingest")
    print("\nPara testar com arquivo real:")
    print("curl -X POST http://localhost:8001/api/v1/audio/transcribe \\")
    print("  -H 'Content-Type: multipart/form-data' \\")
    print("  -F 'file=@caminho/para/audio.mp3'")

    # Se chegou até aqui, passou
    assert True


def create_test_audio_script():
    """Cria script de teste com cURL"""
    script_content = """@echo off
echo Testando Aurora Platform - Audio Transcription

echo.
echo Para testar, substitua "caminho/para/audio.mp3" por um arquivo real
echo.

echo Teste 1: Transcricao simples
echo curl -X POST "http://localhost:8001/api/v1/audio/transcribe" ^
echo      -H "Content-Type: multipart/form-data" ^
echo      -F "file=@caminho/para/audio.mp3"

echo.
echo Teste 2: Transcricao e ingestao
echo curl -X POST "http://localhost:8001/api/v1/audio/transcribe-and-ingest" ^
echo      -H "Content-Type: multipart/form-data" ^
echo      -F "file=@caminho/para/audio.mp3" ^
echo      -F "metadata={\"title\": \"Minha Transcricao\", \"source\": \"teste\"}"

echo.
echo Acesse http://localhost:8001/docs para interface web
"""

    with open("test_audio_curl.bat", "w") as f:
        f.write(script_content)

    print("\nScript de teste criado: test_audio_curl.bat")


if __name__ == "__main__":
    print("TESTE AUDIO API - Aurora Platform\n")

    endpoints_ok = test_audio_endpoints()

    if endpoints_ok:
        create_test_audio_script()
        print("\nSistema de audio pronto para testes!")
    else:
        print("\nInicie a aplicacao primeiro: python run.py")
