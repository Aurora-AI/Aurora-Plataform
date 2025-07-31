#!/bin/bash

# Garante que o Uvicorn está instalado no venv

if [ -x /app/.venv/bin/uvicorn ]; then
    # Executa usando o venv
    /app/.venv/bin/uvicorn src.aurora_platform.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "⚠️ .venv ou uvicorn não encontrado, usando Python/pip do sistema."
    pip install uvicorn fastapi
    uvicorn src.aurora_platform.main:app --host 0.0.0.0 --port 8000 --reload
fi
