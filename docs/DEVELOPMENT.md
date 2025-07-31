# Guia de Desenvolvimento - Aurora-Plataform

## 🚀 Setup do Ambiente de Desenvolvimento

### Pré-requisitos
- **Python:** 3.11 ou superior
- **Poetry:** Gerenciador de dependências
- **Docker:** Para execução de serviços de apoio
- **Git:** Controle de versão

### Configuração Inicial

#### 1. Clone e Setup Básico
```bash
# Clone o repositório
git clone https://github.com/Aurora-AI/Aurora-Plataform.git
cd Aurora-Plataform

# Execute o script de setup (a ser criado)
./scripts/setup.sh
```

#### 2. Configuração por Módulo

##### Aurora-Core
```bash
cd aurora-core

# Instalar dependências
poetry install

# Configurar ambiente
cp .env.example .env
cp config/settings.example.toml config/settings.toml
cp config/.secrets.example.toml config/.secrets.toml

# Configurar banco de dados
poetry run alembic upgrade head

# Iniciar servidor de desenvolvimento
poetry run uvicorn src.aurora_platform.main:app --reload --port 8080
```

##### Aurora-Crawler
```bash
cd aurora-crawler

# Instalar dependências
poetry install

# Configurar ambiente
cp .env.example .env

# Executar aplicação
poetry run python run.py
```

## 🛠️ Ferramentas de Desenvolvimento

### Formatação e Linting
```bash
# Aurora-Core
cd aurora-core
poetry run ruff check .
poetry run ruff format .
poetry run mypy src/

# Aurora-Crawler
cd aurora-crawler
poetry run ruff check .
poetry run ruff format .
```

### Testes
```bash
# Executar todos os testes
./scripts/test-all.sh

# Testes por módulo
cd aurora-core && poetry run pytest
cd aurora-crawler && poetry run pytest

# Testes com coverage
cd aurora-core && poetry run pytest --cov=src/
```

## 🏗️ Estrutura de Desenvolvimento

### Convenções de Nomenclatura

#### Arquivos e Diretórios:
- `snake_case` para arquivos Python
- `kebab-case` para diretórios de projeto
- `PascalCase` para classes
- `UPPER_CASE` para constantes

#### Git Branches:
- `main` - Branch principal
- `develop` - Desenvolvimento integrado
- `feature/nome-da-feature` - Novas funcionalidades
- `hotfix/nome-do-fix` - Correções críticas
- `release/v1.0.0` - Preparação de releases

### Estrutura de Commits:
```
type(scope): description

feat(auth): add JWT refresh token functionality
fix(crawler): resolve memory leak in batch processing
docs(readme): update installation instructions
test(api): add integration tests for user endpoints
```

## 🧪 Testing Guidelines

### Estrutura de Testes
```
tests/
├── unit/           # Testes unitários
├── integration/    # Testes de integração
├── e2e/           # Testes end-to-end
└── fixtures/      # Dados de teste
```

### Tipos de Teste

#### Unit Tests:
```python
# Exemplo: test_auth_service.py
import pytest
from src.aurora_platform.services.auth_service import verify_password

def test_verify_password_valid():
    hashed = get_password_hash("secret123")
    assert verify_password("secret123", hashed) is True

def test_verify_password_invalid():
    hashed = get_password_hash("secret123")
    assert verify_password("wrong", hashed) is False
```

#### Integration Tests:
```python
# Exemplo: test_api_integration.py
import pytest
from fastapi.testclient import TestClient
from src.aurora_platform.main import app

client = TestClient(app)

def test_auth_flow():
    # Test login
    response = client.post("/auth/token", data={
        "username": "test",
        "password": "test123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Test protected endpoint
    response = client.get("/protected", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
```

### Mocking e Fixtures:
```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_database():
    return Mock()

@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
```

## 🔧 Configuração de Ambiente

### Variáveis de Ambiente

#### Aurora-Core (.env):
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/aurora_core
POSTGRES_USER=aurora_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=aurora_core

# Redis
REDIS_URL=redis://localhost:6379

# ChromaDB
CHROMA_URL=http://localhost:8000

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

#### Aurora-Crawler (.env):
```bash
# Chrome Driver
CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
HEADLESS_MODE=true

# Output
OUTPUT_DIR=./outputs
LOG_LEVEL=INFO

# Rate Limiting
REQUEST_DELAY=1
MAX_RETRIES=3
```

## 🐳 Docker Development

### Desenvolvimento com Docker:
```bash
# Iniciar todos os serviços
docker-compose up -d

# Apenas serviços de apoio (DB, Redis, ChromaDB)
docker-compose up -d postgresql redis chromadb

# Logs dos serviços
docker-compose logs -f aurora-core
```

### Rebuild após mudanças:
```bash
# Rebuild específico
docker-compose build aurora-core

# Rebuild completo
docker-compose build --no-cache
```

## 📊 Debugging

### Local Debugging:
```python
# Adicionar breakpoints
import pdb; pdb.set_trace()

# Logging personalizado
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message here")
```

### Docker Debugging:
```bash
# Acessar container
docker-compose exec aurora-core bash

# Ver logs detalhados
docker-compose logs --tail=100 aurora-core

# Debug de rede
docker-compose exec aurora-core ping chromadb
```

## 🚀 Deploy e Release

### Processo de Release:
1. Atualizar versões em `pyproject.toml`
2. Atualizar `CHANGELOG.md`
3. Criar tag de release: `git tag v1.0.0`
4. Push da tag: `git push origin v1.0.0`
5. Deploy automatizado via CI/CD

### Build de Produção:
```bash
# Build das imagens
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Code Review Guidelines

### Checklist de PR:
- [ ] Código segue as convenções de estilo
- [ ] Testes implementados e passando
- [ ] Documentação atualizada
- [ ] Sem secrets expostos
- [ ] Performance considerada
- [ ] Backward compatibility mantida

### Review Process:
1. Automated checks (CI/CD)
2. Code review por peers
3. Approval de maintainer
4. Merge para develop
5. Testing em staging
6. Merge para main

## 🔍 Performance Monitoring

### Profiling:
```python
# Line profiling
@profile
def expensive_function():
    # code here
    pass

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    # code here
    pass
```

### Database Optimization:
```python
# Query optimization
from sqlalchemy import text

# Use raw SQL para queries complexas
result = session.execute(text("SELECT * FROM users WHERE created_at > :date"), 
                        {"date": datetime.now()})

# Index monitoring
# Adicionar logs de query time
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

---

**Mantenha este documento atualizado conforme novas práticas são estabelecidas!**