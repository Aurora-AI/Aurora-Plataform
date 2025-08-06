# 🚀 Aurora Platform - Sistema Operacional de IA (AIOS)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🌟 Visão Geral

Aurora Platform é um Sistema Operacional de Inteligência Artificial (AIOS) moderno e escalável, projetado para orquestrar e gerenciar múltiplos serviços de IA em uma arquitetura distribuída. O projeto consolida as principais inovações em IA, oferecendo uma plataforma unificada para desenvolvimento, deployment e operação de soluções inteligentes.

## 🏗️ Arquitetura Multi-Serviço

```
Aurora Platform
├── Aurora-Core/              # 🎯 Aplicação principal
│   ├── API Gateway           # 🔌 Endpoints unificados
│   ├── Authentication       # 🔐 JWT + OAuth2
│   ├── LLM Integration      # 🧠 Large Language Models
│   └── Knowledge Base       # 📚 RAG + Vector DB
├── Redis/                   # ⚡ Cache e sessões
├── ChromaDB/                # 🔍 Vector database
├── PostgreSQL/              # 💾 Banco principal
└── Nginx/                   # 🌐 Reverse proxy
```

## ✨ Funcionalidades Principais

### 🤖 Aurora-LLM
- **Multi-Model Support**: Integração com GPT, Claude, Phi-3, e modelos locais
- **Intelligent Routing**: Seleção automática do melhor modelo para cada tarefa
- **Context Management**: Gerenciamento avançado de contexto e memória
- **Performance Optimization**: Cache inteligente e rate limiting

### 🛡️ Segurança e Governança
- **JWT Authentication**: Autenticação robusta com refresh tokens
- **Rate Limiting**: Proteção contra abuso e DDoS
- **Monitoring**: Sentry integration para error tracking
- **Compliance**: LGPD/GDPR ready

### 📊 Observabilidade
- **Health Checks**: Monitoramento proativo de todos os serviços
- **Structured Logging**: Logs centralizados e estruturados
- **Performance Metrics**: Dashboards de performance em tempo real
- **Error Tracking**: Rastreamento automático de erros e exceções

## 🚀 Quick Start

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+
- Git

### 1. Clone o Repositório
```bash
git clone https://github.com/Aurora-AI/Aurora-Plataform.git
cd Aurora-Plataform
```

### 2. Configuração do Ambiente
```bash
# Copie o arquivo de configuração
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

### 3. Configurações Obrigatórias
Edite o arquivo `.env` e configure:
```bash
# Chaves de API (obrigatórias)
GEMINI_API_KEY=your-gemini-api-key-here
DEEPSEEK_API_KEY=your-deepseek-api-key-here
FIRECRAWL_API_KEY=your-firecrawl-api-key-here

# Segurança
SECRET_KEY=your-super-secret-key-change-in-production

# Google Cloud
GOOGLE_CLOUD_PROJECT=your-gcp-project-id

# Sentry (opcional, mas recomendado)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

### 4. Iniciar a Plataforma
```bash
# Inicia todos os serviços
docker-compose up -d

# Verifica o status dos serviços
docker-compose ps

# Visualiza os logs
docker-compose logs -f aurora-core
```

### 5. Acessar a Aplicação
- **API Docs**: http://localhost/docs
- **Health Check**: http://localhost/health
- **ChromaDB**: http://localhost:8000 (interno)

## 📋 Checklist de Validação

### ✅ Aurora-Core Funcional e Unificado
- [x] Aplicação FastAPI iniciando corretamente
- [x] Endpoints de autenticação funcionais
- [x] Integração LLM operacional
- [x] Knowledge base conectada

### ✅ Docker Compose Validado
- [x] Todos os serviços iniciando sem erros
- [x] Health checks passando
- [x] Network interno funcionando
- [x] Volumes persistentes configurados

### ✅ Configurações Centralizadas
- [x] Arquivo .env.example completo
- [x] config.py unificado
- [x] Variáveis de ambiente validadas
- [x] Secrets management implementado

### ✅ Sentry Integrado e Testado
- [x] Error tracking inicializado
- [x] Performance monitoring ativo
- [x] Logging integration configurada
- [x] Environment filtering implementado

### ✅ Roadmap Aurora-LLM Documentado
- [x] Estratégia de desenvolvimento definida
- [x] Cronograma de implementação
- [x] Componentes técnicos mapeados
- [x] KPIs e métricas estabelecidas

### ✅ Estado do Repositório Preservado
- [x] MIGRATION_COMPLETE.md registrado
- [x] Histórico de commits preservado
- [x] Checklist de governança criado
- [x] Documentação atualizada

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
Aurora-Plataform/
├── aurora-core/                    # Core da aplicação
│   ├── src/aurora_platform/        # Código principal
│   │   ├── api/v1/endpoints/       # API endpoints
│   │   ├── core/                   # Configurações centrais
│   │   ├── services/               # Serviços de negócio
│   │   └── main.py                 # FastAPI app
│   ├── tests/                      # Testes automatizados
│   └── pyproject.toml              # Dependências Python
├── docs/                           # Documentação
│   ├── AURORA_LLM_ROADMAP.md      # Roadmap estratégico
│   └── AURORA_CORE_GOVERNANCE_CHECKLIST.md
├── nginx/                          # Configuração Nginx
├── docker-compose.yml              # Orquestração de serviços
└── .env.example                    # Template de configuração
```

### Comandos Úteis

#### Desenvolvimento Local
```bash
# Entrar no container do Aurora-Core
docker-compose exec aurora-core bash

# Executar testes
docker-compose exec aurora-core python -m pytest

# Verificar logs em tempo real
docker-compose logs -f

# Reiniciar um serviço específico
docker-compose restart aurora-core
```

#### Gerenciamento de Dados
```bash
# Backup do banco de dados
docker-compose exec postgres pg_dump -U aurora_user aurora_db > backup.sql

# Reset completo dos dados
docker-compose down -v
docker-compose up -d
```

#### Debugging
```bash
# Conectar ao Redis
docker-compose exec redis redis-cli

# Conectar ao PostgreSQL
docker-compose exec postgres psql -U aurora_user -d aurora_db

# Verificar status do ChromaDB
curl http://localhost:8000/api/v1/heartbeat
```

## 📚 Documentação Adicional

- [📋 Aurora-Core Governance Checklist](docs/AURORA_CORE_GOVERNANCE_CHECKLIST.md)
- [🚀 Aurora-LLM Strategic Roadmap](docs/AURORA_LLM_ROADMAP.md)
- [✅ Migration Complete Report](aurora-core/MIGRATION_COMPLETE.md)
- [🏗️ Architecture Summary](aurora-core/ARCHITECTURE_SUMMARY.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Desenvolvimento
- Siga o [Governance Checklist](docs/AURORA_CORE_GOVERNANCE_CHECKLIST.md)
- Use Conventional Commits
- Mantenha cobertura de testes ≥ 80%
- Documente todas as APIs públicas

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/Aurora-AI/Aurora-Plataform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aurora-AI/Aurora-Plataform/discussions)
- **Documentation**: [Wiki](https://github.com/Aurora-AI/Aurora-Plataform/wiki)

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎯 Status do Projeto

- **Versão**: 1.0.0
- **Status**: ✅ Produção Ready
- **Última Atualização**: Janeiro 2025
- **Próximo Milestone**: Aurora-LLM Phase 2

---

**Desenvolvido com ❤️ pela equipe Aurora-AI**