# Aurora-Plataform: Sistema Operacional de Inteligência Artificial (AIOS)

## 🌟 Visão Geral

O **Aurora-Plataform** é um monorepo unificado que representa nosso **Sistema Operacional de Inteligência Artificial (AIOS)**. Esta plataforma integra todos os componentes essenciais para criar um ecossistema de cognição distribuída e soberania cognitiva.

## 🏗️ Arquitetura do Monorepo

```
Aurora-Plataform/
├── aurora-core/          # Kernel do AIOS - API Backend e Orquestração
├── aurora-crawler/       # Módulo de Percepção - Web Scraping e Ingestão
├── docs/                 # Documentação centralizada
├── scripts/              # Utilitários compartilhados
├── docker-compose.yaml   # Orquestração dos serviços
└── README.md            # Este arquivo
```

## 🧩 Componentes Principais

### Aurora-Core
- **Função:** Kernel do Sistema Operacional de IA
- **Tecnologias:** FastAPI, PostgreSQL, ChromaDB, Redis
- **Responsabilidades:**
  - Orquestração central via AuroraRouter
  - Memória Ativa (RAG) usando ChromaDB
  - Autenticação e segurança
  - APIs de negócio

### Aurora-Crawler
- **Função:** Camada de Percepção e Ingestão
- **Tecnologias:** Python, Selenium, BeautifulSoup
- **Responsabilidades:**
  - Web scraping inteligente
  - Processamento de documentos
  - Ingestão de conhecimento
  - Análise de conteúdo

## 🚀 Como Começar

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- Poetry (para desenvolvimento local)

### Inicialização Rápida
```bash
# Clone o repositório
git clone https://github.com/Aurora-AI/Aurora-Plataform.git
cd Aurora-Plataform

# Inicie todos os serviços
docker-compose up -d

# Acesse as aplicações:
# Aurora-Core: http://localhost:8080/docs
# Aurora-Crawler: http://localhost:8001/docs
```

### Desenvolvimento Local

#### Aurora-Core
```bash
cd aurora-core
poetry install
poetry run alembic upgrade head
poetry run uvicorn src.aurora_platform.main:app --reload --port 8080
```

#### Aurora-Crawler
```bash
cd aurora-crawler
poetry install
poetry run python run.py
```

## 📚 Documentação

- **Arquitetura Técnica:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Guia de Desenvolvimento:** [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- **Blueprint de Unificação:** [docs/UNIFICATION_BLUEPRINT.md](docs/UNIFICATION_BLUEPRINT.md)
- **APIs:** Disponível em `/docs` de cada serviço

## 🛠️ Scripts Utilitários

O diretório `scripts/` contém utilitários compartilhados:
- **setup.sh:** Configuração inicial do ambiente
- **deploy.sh:** Deploy automatizado
- **test-all.sh:** Execução de testes em todos os módulos

## 🔧 Configuração

### Variáveis de Ambiente
Copie e configure os arquivos de exemplo:
```bash
# Aurora-Core
cp aurora-core/.env.example aurora-core/.env

# Aurora-Crawler  
cp aurora-crawler/.env.example aurora-crawler/.env
```

### Banco de Dados
O sistema utiliza PostgreSQL para persistência e ChromaDB para vetorização:
```bash
# Migrações são executadas automaticamente via Docker
# Para desenvolvimento local:
cd aurora-core
poetry run alembic upgrade head
```

## 🧪 Testes

Execute testes de todos os módulos:
```bash
# Via script utilitário
./scripts/test-all.sh

# Ou individualmente:
cd aurora-core && poetry run pytest
cd aurora-crawler && poetry run pytest
```

## 📈 Monitoramento

- **Logs:** Centralizados via Docker Compose
- **Health Checks:** Disponíveis em `/health` de cada serviço
- **Métricas:** ChromaDB: `http://localhost:8000/api/v1/heartbeat`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏢 Aurora AI

Desenvolvido com ❤️ pela equipe Aurora AI para democratizar a inteligência artificial e promover a soberania cognitiva.

---

**Versão:** 1.0.0 | **Status:** Produção | **Última Atualização:** $(date +'%Y-%m-%d')