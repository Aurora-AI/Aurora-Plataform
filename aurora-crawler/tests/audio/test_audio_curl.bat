@echo off
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
echo      -F "metadata={"title": "Minha Transcricao", "source": "teste"}"

echo.
echo Acesse http://localhost:8001/docs para interface web
