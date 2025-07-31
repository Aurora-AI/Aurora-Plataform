@echo off
echo Iniciando servidor ChromaDB...
echo Porta: 8001
echo Diretorio: ./chroma_db
echo.
chroma run --host localhost --port 8001 --path ./chroma_db