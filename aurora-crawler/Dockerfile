# Dockerfile para o ambiente de desenvolvimento e produção da Aurora Crawler POC

# --- Fase 1: Builder ---
# Usa uma imagem base para instalar dependências e otimizar o cache
 # Dockerfile - Versão de DESENVOLVIMENTO
 
 # Usamos uma imagem base completa que facilita a instalação de pacotes
 FROM python:3.13
 
 # Define o diretório de trabalho padrão dentro do contêiner
 WORKDIR /app
 
 # Instala as dependências do sistema em uma única camada:
 # - curl: para baixar o instalador do Poetry
 # - ffmpeg: para o serviço de transcrição de áudio
 # - procps: para utilitários de sistema como 'ps' e 'free'
 RUN apt-get update && apt-get install -y --no-install-recommends \
     curl \
     ffmpeg \
     procps \
     && rm -rf /var/lib/apt/lists/*
 

# Instala o Poetry (gerenciador de dependências)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# --- CORREÇÃO DEFINITIVA ---
# Adiciona o diretório 'src' ao PYTHONPATH.
ENV PYTHONPATH="${PYTHONPATH}:/app/src"
 
 # Copia apenas os arquivos de definição de dependências
 COPY pyproject.toml poetry.lock ./

# Garante README.md para builds resilientes
RUN test -f README.md || echo "# Aurora-Crawler\n\nDocumentação do projeto Aurora-Crawler." > README.md

# Instala TODAS as dependências, incluindo as de desenvolvimento (como pytest)
 # Esta é a correção principal.
 RUN poetry install --no-interaction --no-ansi
 
 # Instala os navegadores para o Playwright
 RUN poetry run playwright install chromium
 
 # Copia o restante do código do projeto para o diretório de trabalho
 COPY . .
