#!/bin/bash

# Aurora-Plataform Development Helper Script
# Provides common development tasks and utilities

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_usage() {
    echo "Aurora-Plataform Development Helper"
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  logs <service>      Show logs for a specific service"
    echo "  shell <service>     Open shell in service container"
    echo "  restart <service>   Restart a specific service"
    echo "  rebuild <service>   Rebuild and restart a service"
    echo "  test <service>      Run tests for a service"
    echo "  health             Check health of all services"
    echo "  clean              Clean up containers and volumes"
    echo "  backup             Backup persistent data"
    echo "  restore <file>     Restore from backup"
    echo ""
    echo "Services: aurora-core, aurora-crawler, redis, chromadb"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show logs for a service
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        print_error "Please specify a service name"
        return 1
    fi
    
    print_info "Showing logs for $service..."
    docker compose logs -f "$service"
}

# Open shell in service container
open_shell() {
    local service=$1
    if [ -z "$service" ]; then
        print_error "Please specify a service name"
        return 1
    fi
    
    print_info "Opening shell in $service container..."
    docker compose exec "$service" bash
}

# Restart a service
restart_service() {
    local service=$1
    if [ -z "$service" ]; then
        print_error "Please specify a service name"
        return 1
    fi
    
    print_info "Restarting $service..."
    docker compose restart "$service"
    print_success "$service restarted"
}

# Rebuild and restart a service
rebuild_service() {
    local service=$1
    if [ -z "$service" ]; then
        print_error "Please specify a service name"
        return 1
    fi
    
    print_info "Rebuilding $service..."
    docker compose stop "$service"
    docker compose build "$service"
    docker compose up -d "$service"
    print_success "$service rebuilt and restarted"
}

# Run tests for a service
run_tests() {
    local service=$1
    if [ -z "$service" ]; then
        print_error "Please specify a service name"
        return 1
    fi
    
    case "$service" in
        "aurora-core")
            print_info "Running Aurora-Core tests..."
            docker compose exec aurora-core poetry run pytest
            ;;
        "aurora-crawler")
            print_info "Running Aurora-Crawler tests..."
            docker compose exec aurora-crawler poetry run pytest
            ;;
        *)
            print_error "Tests not available for $service"
            return 1
            ;;
    esac
}

# Check health of all services
check_health() {
    print_info "Checking service health..."
    echo ""
    
    services=("aurora-core" "aurora-crawler" "redis" "chromadb")
    
    for service in "${services[@]}"; do
        if docker compose ps "$service" | grep -q "Up"; then
            echo -e "${GREEN}✓${NC} $service is running"
        else
            echo -e "${RED}✗${NC} $service is not running"
        fi
    done
    
    echo ""
    print_info "Service status:"
    docker compose ps
}

# Clean up containers and volumes
clean_environment() {
    print_info "Cleaning up Aurora environment..."
    
    read -p "This will remove all containers and volumes. Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose down -v
        docker system prune -f
        print_success "Environment cleaned"
    else
        print_info "Cleanup cancelled"
    fi
}

# Backup persistent data
backup_data() {
    print_info "Creating backup of persistent data..."
    
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup ChromaDB data
    if docker volume ls | grep -q "aurora-chroma-data"; then
        docker run --rm -v aurora-chroma-data:/source -v "$(pwd)/$backup_dir":/backup alpine tar czf /backup/chroma-data.tar.gz -C /source .
        print_success "ChromaDB data backed up to $backup_dir/chroma-data.tar.gz"
    fi
    
    # Backup Redis data
    if docker volume ls | grep -q "aurora-redis-data"; then
        docker run --rm -v aurora-redis-data:/source -v "$(pwd)/$backup_dir":/backup alpine tar czf /backup/redis-data.tar.gz -C /source .
        print_success "Redis data backed up to $backup_dir/redis-data.tar.gz"
    fi
    
    print_success "Backup completed in $backup_dir"
}

# Restore from backup
restore_data() {
    local backup_file=$1
    if [ -z "$backup_file" ]; then
        print_error "Please specify a backup file"
        return 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        return 1
    fi
    
    print_info "Restoring from backup: $backup_file"
    print_error "Restore functionality not yet implemented"
    # TODO: Implement restore logic
}

# Main command processing
case "${1:-}" in
    "logs")
        show_logs "$2"
        ;;
    "shell")
        open_shell "$2"
        ;;
    "restart")
        restart_service "$2"
        ;;
    "rebuild")
        rebuild_service "$2"
        ;;
    "test")
        run_tests "$2"
        ;;
    "health")
        check_health
        ;;
    "clean")
        clean_environment
        ;;
    "backup")
        backup_data
        ;;
    "restore")
        restore_data "$2"
        ;;
    *)
        print_usage
        ;;
esac