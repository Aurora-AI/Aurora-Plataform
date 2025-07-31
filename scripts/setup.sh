#!/bin/bash

# setup.sh - Script de configuração inicial do Aurora-Plataform
# Executa a configuração completa do ambiente de desenvolvimento

set -e  # Exit on any error

echo "🌟 Aurora-Plataform Setup Script 🌟"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    if ! command_exists python3; then
        log_error "Python 3 não encontrado. Instale Python 3.11 ou superior."
        exit 1
    fi
    
    if ! command_exists poetry; then
        log_error "Poetry não encontrado. Instale: curl -sSL https://install.python-poetry.org | python3 -"
        exit 1
    fi
    
    if ! command_exists docker; then
        log_warning "Docker não encontrado. Instale para usar containers."
    fi
    
    log_success "Pré-requisitos verificados!"
}

# Setup Aurora-Core
setup_aurora_core() {
    log_info "Configurando Aurora-Core..."
    
    cd aurora-core
    
    # Install dependencies
    log_info "Instalando dependências do Aurora-Core..."
    poetry install
    
    # Setup environment files
    if [ ! -f .env ]; then
        log_info "Criando arquivo .env do Aurora-Core..."
        cp .env.example .env
        log_warning "Configure o arquivo aurora-core/.env com suas credenciais!"
    fi
    
    if [ ! -f config/settings.toml ]; then
        log_info "Criando arquivo de configuração..."
        cp config/settings.example.toml config/settings.toml
    fi
    
    if [ ! -f config/.secrets.toml ]; then
        log_info "Criando arquivo de secrets..."
        cp config/.secrets.example.toml config/.secrets.toml
        log_warning "Configure o arquivo aurora-core/config/.secrets.toml!"
    fi
    
    cd ..
    log_success "Aurora-Core configurado!"
}

# Setup Aurora-Crawler
setup_aurora_crawler() {
    log_info "Configurando Aurora-Crawler..."
    
    cd aurora-crawler
    
    # Install dependencies
    log_info "Instalando dependências do Aurora-Crawler..."
    poetry install
    
    # Setup environment files
    if [ ! -f .env ]; then
        log_info "Criando arquivo .env do Aurora-Crawler..."
        cp .env.example .env
        log_warning "Configure o arquivo aurora-crawler/.env conforme necessário!"
    fi
    
    cd ..
    log_success "Aurora-Crawler configurado!"
}

# Setup Docker environment
setup_docker() {
    if command_exists docker && command_exists docker-compose; then
        log_info "Configurando ambiente Docker..."
        
        # Pull necessary images
        docker-compose pull
        
        log_success "Ambiente Docker configurado!"
    else
        log_warning "Docker não disponível. Pule para desenvolvimento local."
    fi
}

# Setup database
setup_database() {
    log_info "Configurando banco de dados..."
    
    if command_exists docker; then
        log_info "Iniciando serviços de apoio (PostgreSQL, Redis, ChromaDB)..."
        docker-compose up -d postgresql redis chromadb
        
        # Wait a bit for services to start
        sleep 10
        
        # Run migrations
        log_info "Executando migrações do banco de dados..."
        cd aurora-core
        poetry run alembic upgrade head
        cd ..
        
        log_success "Banco de dados configurado!"
    else
        log_warning "Configure manualmente PostgreSQL, Redis e ChromaDB para desenvolvimento local."
    fi
}

# Create development shortcuts
create_shortcuts() {
    log_info "Criando scripts de atalho..."
    
    # Create start script
    cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Aurora-Plataform em modo desenvolvimento..."

# Start support services
docker-compose up -d postgresql redis chromadb

# Start Aurora-Core in background
cd aurora-core
poetry run uvicorn src.aurora_platform.main:app --reload --port 8080 &
CORE_PID=$!
cd ..

# Start Aurora-Crawler
cd aurora-crawler
poetry run python run.py &
CRAWLER_PID=$!
cd ..

echo "✅ Serviços iniciados:"
echo "   Aurora-Core: http://localhost:8080/docs"
echo "   Aurora-Crawler: http://localhost:8001"

# Wait for interrupt
trap "kill $CORE_PID $CRAWLER_PID; exit" INT
wait
EOF
    
    chmod +x start-dev.sh
    
    log_success "Scripts de atalho criados!"
}

# Main setup process
main() {
    echo ""
    log_info "Iniciando configuração do Aurora-Plataform..."
    echo ""
    
    check_prerequisites
    setup_aurora_core
    setup_aurora_crawler
    setup_docker
    setup_database
    create_shortcuts
    
    echo ""
    log_success "🎉 Setup completo!"
    echo ""
    echo "Próximos passos:"
    echo "1. Configure os arquivos .env nos diretórios aurora-core/ e aurora-crawler/"
    echo "2. Execute: ./start-dev.sh para iniciar o ambiente de desenvolvimento"
    echo "3. Acesse: http://localhost:8080/docs para ver a API do Aurora-Core"
    echo ""
    echo "Para mais informações, consulte: docs/DEVELOPMENT.md"
}

# Run main function
main "$@"