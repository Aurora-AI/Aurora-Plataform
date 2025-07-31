# Aurora-Plataform Scripts 🔧

This directory contains shared utilities and scripts for the Aurora-Plataform monorepo.

## Available Scripts

### 🚀 `setup.sh`
**Purpose**: Initialize the Aurora-Plataform development environment

**Usage**:
```bash
# Full setup (recommended for first-time setup)
./scripts/setup.sh

# Check prerequisites and configuration only
./scripts/setup.sh check

# Setup environment files only
./scripts/setup.sh env

# Start services only
./scripts/setup.sh start

# Show service status
./scripts/setup.sh status
```

**What it does**:
- Validates Docker and Docker Compose installation
- Creates `.env` files from templates
- Validates Docker Compose configuration
- Builds and starts all services
- Shows service status and access URLs

### 🛠️ `dev-helper.sh`
**Purpose**: Development utilities and common tasks

**Usage**:
```bash
# Show logs for a service
./scripts/dev-helper.sh logs aurora-core
./scripts/dev-helper.sh logs aurora-crawler

# Open shell in service container
./scripts/dev-helper.sh shell aurora-core
./scripts/dev-helper.sh shell aurora-crawler

# Restart a service
./scripts/dev-helper.sh restart aurora-core

# Rebuild and restart a service
./scripts/dev-helper.sh rebuild aurora-crawler

# Run tests
./scripts/dev-helper.sh test aurora-core
./scripts/dev-helper.sh test aurora-crawler

# Check health of all services
./scripts/dev-helper.sh health

# Clean up environment (removes containers and volumes)
./scripts/dev-helper.sh clean

# Backup persistent data
./scripts/dev-helper.sh backup

# Restore from backup (future feature)
./scripts/dev-helper.sh restore backup-file.tar.gz
```

## Quick Start Workflow

### First-time Setup
```bash
# 1. Run full setup
./scripts/setup.sh

# 2. Edit environment files with your configurations
nano aurora-core/.env
nano aurora-crawler/.env

# 3. Restart services with new configuration
./scripts/dev-helper.sh restart aurora-core
./scripts/dev-helper.sh restart aurora-crawler
```

### Daily Development
```bash
# Check service health
./scripts/dev-helper.sh health

# View logs
./scripts/dev-helper.sh logs aurora-core

# Run tests
./scripts/dev-helper.sh test aurora-core

# Open shell for debugging
./scripts/dev-helper.sh shell aurora-crawler
```

### Troubleshooting
```bash
# Rebuild problematic service
./scripts/dev-helper.sh rebuild aurora-core

# Clean environment and start fresh
./scripts/dev-helper.sh clean
./scripts/setup.sh
```

## Adding New Scripts

When adding new scripts to this directory:

1. **Follow naming convention**: Use descriptive names with hyphens (e.g., `data-migration.sh`)
2. **Make executable**: `chmod +x scripts/your-script.sh`
3. **Add documentation**: Update this README with script description
4. **Use consistent styling**: Follow the color coding and output format used in existing scripts
5. **Error handling**: Use `set -e` and proper error checking
6. **Help/usage**: Include usage instructions in the script

## Script Development Guidelines

### Color Coding
```bash
RED='\033[0;31m'     # Errors
GREEN='\033[0;32m'   # Success messages
YELLOW='\033[1;33m'  # Warnings
BLUE='\033[0;34m'    # Info messages
NC='\033[0m'         # No Color
```

### Output Functions
```bash
print_info() {
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
```

### Error Handling
```bash
# Enable strict error handling
set -e

# Check prerequisites
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi
```

## Future Scripts

Planned additions to this directory:

- **`migrate.sh`**: Database migration utilities
- **`deploy.sh`**: Production deployment scripts
- **`monitor.sh`**: Health monitoring and alerting
- **`backup-restore.sh`**: Enhanced backup and restore functionality
- **`security-check.sh`**: Security scanning and validation
- **`performance-test.sh`**: Load testing and performance benchmarks

---

*These scripts are designed to make Aurora-Plataform development and operations as smooth as possible. If you encounter issues or have suggestions for improvements, please update this documentation and the scripts accordingly.*