@echo off
echo Instalando dependencias criticas...

pip install openai-whisper
pip install pymupdf
pip install python-docx
pip install ffmpeg-python

echo.
echo Verificando instalacao do FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo AVISO: FFmpeg nao encontrado no sistema
    echo Baixe em: https://ffmpeg.org/download.html
    echo Ou use: winget install ffmpeg
)

echo.
echo Dependencias instaladas!
pause