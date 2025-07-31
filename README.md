# Aurora-Plataform 🌟

**A Unified Monorepo for the Aurora AI Ecosystem**

Aurora-Plataform is the consolidated monorepo infrastructure that unifies Aurora-Core and Aurora-Crawler into a cohesive, scalable AI platform. This repository implements shared architecture, standardized governance, and orchestrated deployment for the entire Aurora ecosystem.

## 🏗️ Architecture Overview

The Aurora-Plataform monorepo consists of two main applications and shared infrastructure:

### **Aurora-Core** (`./aurora-core/`)
The kernel of our AI Operating System (AIOS) - a FastAPI-based backend that provides:
- Central orchestration via AuroraRouter
- Active Memory (RAG) using ChromaDB
- Deep perception layer with DeepDiveScraper
- AI Factory tools for automated governance
- **Port:** 8080

### **Aurora-Crawler** (`./aurora-crawler/`)
Advanced web crawling and data ingestion service:
- Deep crawling capabilities with Playwright
- Document processing and content extraction
- Audio transcription services
- Batch ingestion systems
- **Port:** 8001

### **Shared Infrastructure**
- **ChromaDB** (Port 8000): Vector database for knowledge storage
- **Redis** (Port 6379): Caching and session management
- **Unified Network**: All services communicate via `aurora-network`

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/Aurora-AI/Aurora-Plataform.git
cd Aurora-Plataform
```

### 2. Environment Configuration
```bash
# Copy environment templates
cp aurora-core/.env.example aurora-core/.env
cp aurora-crawler/.env.example aurora-crawler/.env

# Edit the .env files with your configurations
nano aurora-core/.env
nano aurora-crawler/.env
```

### 3. Start the Platform
```bash
# Build and start all services
docker compose up --build

# Or run in detached mode
docker compose up --build -d
```

### 4. Access Services
- **Aurora-Core API**: http://localhost:8080/docs
- **Aurora-Crawler API**: http://localhost:8001/docs  
- **ChromaDB**: http://localhost:8000
- **Redis**: localhost:6379

## 📁 Project Structure

```
Aurora-Plataform/
├── aurora-core/                 # Core AI platform service
│   ├── src/                     # Source code
│   ├── tests/                   # Test suites
│   ├── docs/                    # Core-specific documentation
│   ├── Dockerfile               # Core service container
│   └── pyproject.toml           # Core dependencies
├── aurora-crawler/              # Crawler and ingestion service
│   ├── src/                     # Source code
│   ├── tests/                   # Test suites
│   ├── docs/                    # Crawler-specific documentation
│   ├── Dockerfile               # Crawler service container
│   └── pyproject.toml           # Crawler dependencies
├── docs/                        # Shared monorepo documentation
│   ├── UNIFICATION_BLUEPRINT.md # Architecture standards
│   └── ARCHITECTURE.md          # System architecture
├── scripts/                     # Shared utilities and scripts
├── docker-compose.yaml          # Unified orchestration
└── README.md                    # This file
```

## 🛠️ Development

### Quick Development Setup
Use the provided setup script for fast initialization:

```bash
# Full setup with environment validation
./scripts/setup.sh

# Development utilities
./scripts/dev-helper.sh health              # Check service status
./scripts/dev-helper.sh logs aurora-core    # View service logs
./scripts/dev-helper.sh shell aurora-core   # Open service shell
./scripts/dev-helper.sh test aurora-core    # Run service tests
```

### Individual Service Development
Each service can be developed independently:

```bash
# Aurora-Core
cd aurora-core
poetry install
poetry run uvicorn src.aurora_platform.main:app --reload

# Aurora-Crawler  
cd aurora-crawler
poetry install
poetry run uvicorn src.main:app --reload
```

### Full Stack Development
Use Docker Compose for full stack development:

```bash
# Development mode with hot reloading
docker compose -f docker-compose.yaml -f docker-compose.override.yml up --build

# Production mode
docker compose up --build

# Rebuild specific service
docker compose up --build aurora-core

# View logs
docker compose logs -f aurora-core
docker compose logs -f aurora-crawler

# Execute commands in running containers
docker compose exec aurora-core bash
docker compose exec aurora-crawler bash
```

## 🔧 Configuration

### Environment Variables
Each service has its own `.env` file with service-specific configurations:

**Aurora-Core** (`aurora-core/.env`):
- Database configurations
- AI service API keys (Gemini, Firecrawl)
- Security settings
- Rate limiting

**Aurora-Crawler** (`aurora-crawler/.env`):
- ChromaDB connection settings
- Scraper configurations
- JWT settings
- File processing limits

### Shared Resources
Services automatically connect to shared infrastructure via the unified Docker network:
- Redis: `redis://redis:6379`
- ChromaDB: `http://chromadb:8000`

### Configuration Consolidation
This monorepo has unified previously separate docker-compose and CI/CD configurations:
- ✅ Removed duplicate docker-compose.yml files from individual services
- ✅ Consolidated GitHub Actions workflows into a single monorepo CI/CD pipeline
- ✅ Unified .gitignore at the root level
- ✅ Preserved all functionality while eliminating duplication

Legacy configuration files are preserved in `docs/legacy/` for reference.

## 📊 Monitoring and Health Checks

All services include health checks and monitoring:

```bash
# Check service health
docker compose ps

# View service logs
docker compose logs

# Monitor resource usage
docker stats
```

## 🧪 Testing

Run tests for individual services:

```bash
# Aurora-Core tests
cd aurora-core
poetry run pytest

# Aurora-Crawler tests  
cd aurora-crawler
poetry run pytest
```

## 📚 Documentation

- **[Architecture Blueprint](./docs/UNIFICATION_BLUEPRINT.md)**: Standards and conventions
- **[Aurora-Core Documentation](./aurora-core/README.md)**: Core service details
- **[Aurora-Crawler Documentation](./aurora-crawler/README.md)**: Crawler service details

## 🤝 Contributing

1. Follow the standards defined in `docs/UNIFICATION_BLUEPRINT.md`
2. Ensure both services start correctly with `docker compose up --build`
3. Add tests for new functionality
4. Update documentation for architectural changes

## 📜 License

MIT License - see individual service directories for specific licensing details.

## 🔗 Related Projects

- [Aurora-Core](./aurora-core/): AI Operating System kernel
- [Aurora-Crawler](./aurora-crawler/): Web crawling and data ingestion

---

**Aurora-Plataform**: Building the future of distributed AI cognition 🚀