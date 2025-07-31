@echo off
echo 🚀 Testando Aurora Platform via cURL

echo.
echo Teste 1: Ingestao Semantica
curl -X POST "http://localhost:8001/api/v1/knowledge/ingest-semantic" ^
     -H "Content-Type: application/json" ^
     -d "{\"url\": \"https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf\"}"

echo.
echo.
echo Teste 2: Busca na Base de Conhecimento
curl -X POST "http://localhost:8001/api/v1/knowledge/search" ^
     -H "Content-Type: application/json" ^
     -d "{\"query\": \"test document\", \"n_results\": 3}"

echo.
echo.
echo ✅ Testes concluídos!