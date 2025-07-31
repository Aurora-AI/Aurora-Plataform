@echo off
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
echo      -F "metadata={"title": "Meu Documento", "source": "teste"}"

echo.
echo Formatos suportados: PDF, DOCX, DOC, TXT
echo Acesse http://localhost:8001/docs para interface web
