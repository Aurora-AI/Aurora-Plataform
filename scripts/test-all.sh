#!/bin/bash

# test-all.sh - Script para executar todos os testes dos módulos Aurora

set -e

echo "🧪 Aurora-Plataform Test Suite 🧪"
echo "================================="

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

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run tests for a module
run_module_tests() {
    local module_name=$1
    local module_dir=$2
    
    log_info "Executando testes para $module_name..."
    
    if [ ! -d "$module_dir" ]; then
        log_error "Diretório $module_dir não encontrado!"
        return 1
    fi
    
    cd "$module_dir"
    
    # Check if poetry.lock exists
    if [ ! -f "poetry.lock" ]; then
        log_warning "poetry.lock não encontrado em $module_dir. Executando poetry install..."
        poetry install
    fi
    
    # Run tests with coverage
    if poetry run pytest --cov=src/ --cov-report=term-missing --cov-report=html --junitxml=test-results.xml -v; then
        log_success "Testes do $module_name passaram!"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        log_error "Testes do $module_name falharam!"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    cd ..
}

# Function to run linting
run_module_lint() {
    local module_name=$1
    local module_dir=$2
    
    log_info "Executando linting para $module_name..."
    
    cd "$module_dir"
    
    # Run ruff check
    if poetry run ruff check .; then
        log_success "Linting do $module_name passou!"
    else
        log_error "Linting do $module_name falhou!"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    
    # Run type checking with mypy (if configured)
    if [ -f "pyproject.toml" ] && grep -q "mypy" pyproject.toml; then
        if poetry run mypy src/; then
            log_success "Type checking do $module_name passou!"
        else
            log_warning "Type checking do $module_name apresentou avisos!"
        fi
    fi
    
    cd ..
}

# Function to generate combined coverage report
generate_coverage_report() {
    log_info "Gerando relatório de cobertura combinado..."
    
    # Create coverage directory
    mkdir -p coverage-reports
    
    # Copy individual coverage reports
    if [ -d "aurora-core/htmlcov" ]; then
        cp -r aurora-core/htmlcov coverage-reports/aurora-core-coverage
    fi
    
    if [ -d "aurora-crawler/htmlcov" ]; then
        cp -r aurora-crawler/htmlcov coverage-reports/aurora-crawler-coverage
    fi
    
    log_success "Relatórios de cobertura salvos em coverage-reports/"
}

# Function to check Docker services health
check_docker_services() {
    log_info "Verificando serviços Docker necessários para testes..."
    
    # Check if docker-compose is available
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_warning "docker-compose não encontrado. Alguns testes de integração podem falhar."
        return
    fi
    
    # Start test services if not running
    if ! docker-compose ps | grep -q "Up"; then
        log_info "Iniciando serviços de teste..."
        docker-compose up -d postgresql redis chromadb
        
        # Wait for services to be ready
        log_info "Aguardando serviços ficarem prontos..."
        sleep 15
    fi
    
    # Health check
    log_info "Verificando saúde dos serviços..."
    if docker-compose ps | grep -q "postgresql.*Up" && \
       docker-compose ps | grep -q "redis.*Up" && \
       docker-compose ps | grep -q "chromadb.*Up"; then
        log_success "Serviços Docker estão prontos!"
    else
        log_warning "Alguns serviços podem não estar funcionando corretamente."
    fi
}

# Main test execution
main() {
    echo ""
    log_info "Iniciando execução completa de testes..."
    echo ""
    
    # Check and start Docker services
    check_docker_services
    
    # Run linting first
    log_info "=== FASE 1: LINTING ==="
    run_module_lint "Aurora-Core" "aurora-core"
    run_module_lint "Aurora-Crawler" "aurora-crawler"
    
    echo ""
    log_info "=== FASE 2: TESTES UNITÁRIOS ==="
    
    # Run tests for each module
    run_module_tests "Aurora-Core" "aurora-core"
    run_module_tests "Aurora-Crawler" "aurora-crawler"
    
    # Generate coverage report
    generate_coverage_report
    
    # Print summary
    echo ""
    log_info "=== RESUMO DOS TESTES ==="
    echo "Total de módulos testados: $TOTAL_TESTS"
    echo -e "Módulos que passaram: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Módulos que falharam: ${RED}$FAILED_TESTS${NC}"
    
    if [ $FAILED_TESTS -eq 0 ]; then
        echo ""
        log_success "🎉 Todos os testes passaram!"
        echo ""
        echo "Relatórios disponíveis:"
        echo "  - Cobertura: coverage-reports/"
        echo "  - JUnit XML: */test-results.xml"
        exit 0
    else
        echo ""
        log_error "❌ Alguns testes falharam!"
        echo ""
        echo "Verifique os logs acima para detalhes dos erros."
        exit 1
    fi
}

# Check if specific module was requested
if [ $# -eq 1 ]; then
    case $1 in
        "core")
            log_info "Executando testes apenas para Aurora-Core..."
            run_module_tests "Aurora-Core" "aurora-core"
            ;;
        "crawler")
            log_info "Executando testes apenas para Aurora-Crawler..."
            run_module_tests "Aurora-Crawler" "aurora-crawler"
            ;;
        "lint")
            log_info "Executando apenas linting..."
            run_module_lint "Aurora-Core" "aurora-core"
            run_module_lint "Aurora-Crawler" "aurora-crawler"
            ;;
        *)
            echo "Uso: $0 [core|crawler|lint]"
            echo "Ou execute sem argumentos para executar todos os testes."
            exit 1
            ;;
    esac
else
    # Run all tests
    main
fi