@echo off
echo Configurando modo CLIENT_SERVER...
set CHROMA_MODE=CLIENT_SERVER
set PYTHONPATH=%CD%\src;%PYTHONPATH%
echo Iniciando Aurora-Core com reload...
echo Diretorio: %CD%
uvicorn aurora_platform.main:app --reload --host 127.0.0.1 --port 8000