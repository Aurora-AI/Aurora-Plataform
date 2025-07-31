#!/bin/bash

# Aurora-Plataform Setup Script
# Initializes the development environment and validates configuration

set -e

echo "🌟 Aurora-Plataform Setup Script"
echo "=================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Setup environment files
setup_environment() {
    print_status "Setting up environment files..."
    
    # Aurora-Core environment
    if [ ! -f "aurora-core/.env" ]; then
        cp aurora-core/.env.example aurora-core/.env
        print_success "Created aurora-core/.env from template"
        print_warning "Please edit aurora-core/.env with your configurations"
    else
        print_status "aurora-core/.env already exists"
    fi
    
    # Aurora-Crawler environment
    if [ ! -f "aurora-crawler/.env" ]; then
        cp aurora-crawler/.env.example aurora-crawler/.env
        print_success "Created aurora-crawler/.env from template"
        print_warning "Please edit aurora-crawler/.env with your configurations"
    else
        print_status "aurora-crawler/.env already exists"
    fi
}

# Validate Docker Compose configuration
validate_compose() {
    print_status "Validating Docker Compose configuration..."
    
    if docker compose config > /dev/null 2>&1; then
        print_success "Docker Compose configuration is valid"
    else
        print_error "Docker Compose configuration has errors"
        docker compose config
        exit 1
    fi
}

# Build and start services
start_services() {
    print_status "Building and starting Aurora services..."
    
    # Build images
    print_status "Building Docker images..."
    docker compose build
    
    # Start services
    print_status "Starting services..."
    docker compose up -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be healthy..."
    sleep 30
    
    # Check service health
    if docker compose ps --services --filter "status=running" | grep -q "aurora-core"; then
        print_success "Aurora-Core is running"
    else
        print_error "Aurora-Core failed to start"
    fi
    
    if docker compose ps --services --filter "status=running" | grep -q "aurora-crawler"; then
        print_success "Aurora-Crawler is running"
    else
        print_error "Aurora-Crawler failed to start"
    fi
}

# Display service information
show_services() {
    echo ""
    print_status "Aurora-Plataform Services:"
    echo "=========================="
    echo "🎯 Aurora-Core API:     http://localhost:8080/docs"
    echo "🕷️  Aurora-Crawler API:  http://localhost:8001/docs"
    echo "🔍 ChromaDB:           http://localhost:8000"
    echo "🔴 Redis:              localhost:6379"
    echo ""
    print_status "Service Status:"
    docker compose ps
}

# Main execution
main() {
    check_prerequisites
    setup_environment
    validate_compose
    start_services
    show_services
    
    echo ""
    print_success "Aurora-Plataform setup completed!"
    print_status "Use 'docker compose logs -f' to view service logs"
    print_status "Use 'docker compose down' to stop all services"
}

# Handle script arguments
case "${1:-}" in
    "check")
        check_prerequisites
        validate_compose
        ;;
    "env")
        setup_environment
        ;;
    "start")
        start_services
        ;;
    "status")
        show_services
        ;;
    *)
        main
        ;;
esac