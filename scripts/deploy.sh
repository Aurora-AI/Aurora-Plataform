#!/bin/bash

# deploy.sh - Script de deploy do Aurora-Plataform
# Executa o deploy completo da plataforma em diferentes ambientes

set -e

echo "🚀 Aurora-Plataform Deploy Script 🚀"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT="development"
BUILD_IMAGES="true"
PULL_LATEST="false"
BACKUP_DATA="false"

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

# Show usage
show_usage() {
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Opções:"
    echo "  -e, --environment ENV    Ambiente de deploy (development|staging|production) [default: development]"
    echo "  -b, --build             Força rebuild das imagens Docker"
    echo "  -p, --pull              Pull das imagens mais recentes"
    echo "  --backup                Cria backup dos dados antes do deploy"
    echo "  --no-build              Não rebuilda as imagens"
    echo "  -h, --help              Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0                                    # Deploy desenvolvimento"
    echo "  $0 -e production --backup            # Deploy produção com backup"
    echo "  $0 -e staging --pull                 # Deploy staging com pull"
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -b|--build)
                BUILD_IMAGES="true"
                shift
                ;;
            --no-build)
                BUILD_IMAGES="false"
                shift
                ;;
            -p|--pull)
                PULL_LATEST="true"
                shift
                ;;
            --backup)
                BACKUP_DATA="true"
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Opção desconhecida: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Validate environment
validate_environment() {
    case $ENVIRONMENT in
        development|staging|production)
            log_info "Ambiente selecionado: $ENVIRONMENT"
            ;;
        *)
            log_error "Ambiente inválido: $ENVIRONMENT"
            log_error "Ambientes válidos: development, staging, production"
            exit 1
            ;;
    esac
}

# Check prerequisites
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    if ! command -v docker >/dev/null 2>&1; then
        log_error "Docker não encontrado. Instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker Compose não encontrado. Instale o Docker Compose primeiro."
        exit 1
    fi
    
    # Check if docker-compose file exists
    local compose_file="docker-compose.yaml"
    if [ "$ENVIRONMENT" != "development" ]; then
        compose_file="docker-compose.$ENVIRONMENT.yml"
    fi
    
    if [ ! -f "$compose_file" ]; then
        log_warning "Arquivo $compose_file não encontrado. Usando docker-compose.yaml padrão."
        compose_file="docker-compose.yaml"
    fi
    
    COMPOSE_FILE="$compose_file"
    log_success "Pré-requisitos verificados!"
}

# Backup data
backup_data() {
    if [ "$BACKUP_DATA" = "true" ]; then
        log_info "Criando backup dos dados..."
        
        local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        
        # Backup PostgreSQL
        if docker-compose ps | grep -q "postgresql.*Up"; then
            log_info "Criando backup do PostgreSQL..."
            docker-compose exec -T postgresql pg_dump -U aurora_user aurora_core > "$backup_dir/postgresql_backup.sql"
        fi
        
        # Backup ChromaDB
        if docker-compose ps | grep -q "chromadb.*Up"; then
            log_info "Criando backup do ChromaDB..."
            docker-compose exec chromadb tar czf - /chroma/chroma > "$backup_dir/chromadb_backup.tar.gz"
        fi
        
        log_success "Backup criado em: $backup_dir"
    fi
}

# Stop services
stop_services() {
    log_info "Parando serviços existentes..."
    docker-compose -f "$COMPOSE_FILE" down
    log_success "Serviços parados!"
}

# Pull images
pull_images() {
    if [ "$PULL_LATEST" = "true" ]; then
        log_info "Fazendo pull das imagens mais recentes..."
        docker-compose -f "$COMPOSE_FILE" pull
        log_success "Images atualizadas!"
    fi
}

# Build images
build_images() {
    if [ "$BUILD_IMAGES" = "true" ]; then
        log_info "Construindo imagens Docker..."
        docker-compose -f "$COMPOSE_FILE" build --no-cache
        log_success "Imagens construídas!"
    fi
}

# Start services
start_services() {
    log_info "Iniciando serviços..."
    
    # Start infrastructure services first
    log_info "Iniciando serviços de infraestrutura..."
    docker-compose -f "$COMPOSE_FILE" up -d postgresql redis chromadb
    
    # Wait for infrastructure to be ready
    log_info "Aguardando serviços de infraestrutura ficarem prontos..."
    sleep 30
    
    # Start application services
    log_info "Iniciando serviços de aplicação..."
    docker-compose -f "$COMPOSE_FILE" up -d aurora-core aurora-crawler
    
    log_success "Serviços iniciados!"
}

# Wait for services to be healthy
wait_for_health() {
    log_info "Verificando saúde dos serviços..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        local healthy=true
        
        # Check Aurora-Core
        if ! curl -f http://localhost:8080/health >/dev/null 2>&1; then
            healthy=false
        fi
        
        # Check Aurora-Crawler
        if ! curl -f http://localhost:8001/health >/dev/null 2>&1; then
            healthy=false
        fi
        
        if [ "$healthy" = "true" ]; then
            log_success "Todos os serviços estão saudáveis!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        log_info "Tentativa $attempt/$max_attempts - Aguardando serviços ficarem prontos..."
        sleep 10
    done
    
    log_warning "Alguns serviços podem não estar completamente prontos. Verifique os logs."
}

# Show deployment info
show_deployment_info() {
    echo ""
    log_success "🎉 Deploy concluído!"
    echo ""
    echo "Informações do deployment:"
    echo "  Ambiente: $ENVIRONMENT"
    echo "  Arquivo Compose: $COMPOSE_FILE"
    echo ""
    echo "Serviços disponíveis:"
    echo "  Aurora-Core API: http://localhost:8080/docs"
    echo "  Aurora-Crawler: http://localhost:8001"
    echo "  ChromaDB: http://localhost:8000"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis: localhost:6379"
    echo ""
    echo "Comandos úteis:"
    echo "  docker-compose -f $COMPOSE_FILE logs -f          # Ver logs"
    echo "  docker-compose -f $COMPOSE_FILE ps              # Status dos serviços"
    echo "  docker-compose -f $COMPOSE_FILE down            # Parar tudo"
    echo ""
}

# Main deploy process
main() {
    parse_args "$@"
    validate_environment
    check_prerequisites
    backup_data
    stop_services
    pull_images
    build_images
    start_services
    wait_for_health
    show_deployment_info
}

# Run main function
main "$@"