import requests
import json

# Configuração
BASE_URL = "http://localhost:8001/api/v1/documents"


def test_document_endpoints():
    """Testa se os endpoints de documentos estão disponíveis"""

    print("Testando disponibilidade dos endpoints de documentos...")

    # Teste de conectividade básica
    try:
        response = requests.get("http://localhost:8001/docs")
        assert response.status_code == 200, "Aplicação não está rodando"
        print("OK Aplicação está rodando")
    except requests.exceptions.ConnectionError:
        print("ERRO Aplicação não está rodando em localhost:8001")
        print("Execute: python run.py")
        assert False, "Aplicação não está rodando em localhost:8001"

    print("\nEndpoints de documentos disponíveis:")
    print("- POST /api/v1/documents/extract-text")
    print("- POST /api/v1/documents/process-and-ingest")
    print("\nFormatos suportados: PDF, DOCX, DOC, TXT")
    print("\nPara testar com arquivo real:")
    print("curl -X POST http://localhost:8001/api/v1/documents/extract-text \\")
    print("  -H 'Content-Type: multipart/form-data' \\")
    print("  -F 'file=@caminho/para/documento.pdf'")

    # Se chegou até aqui, passou
    assert True


def create_test_document_script():
    """Cria script de teste com cURL"""
    script_content = """@echo off
echo Testando Aurora Platform - Document Processing

echo.
echo Para testar, substitua "caminho/para/documento.pdf" por um arquivo real
echo.

echo Teste 1: Extração de texto
echo curl -X POST "http://localhost:8001/api/v1/documents/extract-text" ^
echo      -H "Content-Type: multipart/form-data" ^
echo      -F "file=@caminho/para/documento.pdf"

echo.
echo Teste 2: Processamento e ingestão
echo curl -X POST "http://localhost:8001/api/v1/documents/process-and-ingest" ^
echo      -H "Content-Type: multipart/form-data" ^
echo      -F "file=@caminho/para/documento.pdf" ^
echo      -F "metadata={\"title\": \"Meu Documento\", \"source\": \"teste\"}"

echo.
echo Formatos suportados: PDF, DOCX, DOC, TXT
echo Acesse http://localhost:8001/docs para interface web
"""

    with open("test_document_curl.bat", "w") as f:
        f.write(script_content)

    print("\nScript de teste criado: test_document_curl.bat")


if __name__ == "__main__":
    print("TESTE DOCUMENT API - Aurora Platform\n")

    endpoints_ok = test_document_endpoints()

    if endpoints_ok:
        create_test_document_script()
        print("\nSistema de documentos pronto para testes!")
    else:
        print("\nInicie a aplicacao primeiro: python run.py")
