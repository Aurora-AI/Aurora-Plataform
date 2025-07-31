@echo off
echo 🚀 Aurora Platform - Instalação e Teste Automatizado

echo.
echo 📦 Instalando dependências...
poetry install --no-root

echo.
echo 🔄 Verificando se ChromaDB está rodando...
timeout /t 2 >nul

echo.
echo 🚀 Iniciando aplicação Aurora...
echo Acesse http://localhost:8000/docs para testar via interface web
echo.
python run.py