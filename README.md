# Aurora-Plataform

> **Sistema Operacional de Inteligência Artificial (AIOS) Aurora**  
> Monorepo oficial da plataforma Aurora - Arquitetura v2

## 🎯 Visão Geral

O Aurora-Plataform é o monorepo que centraliza todos os componentes do **Sistema Operacional de IA Aurora**, representando a evolução e consolidação da nossa arquitetura em uma única plataforma robusta e escalável.

### Arquitetura Principal

```
Aurora-Plataform/
├── aurora-core/          # 🧠 Kernel do AIOS Aurora
│   ├── src/              # FastAPI + SQLModel + Alembic
│   ├── tests/            # Suíte de testes automatizados
│   └── config/           # Configurações multi-ambiente
├── docs/                 # 📚 Documentação técnica
├── .github/workflows/    # 🚀 CI/CD automatizado
└── sanitize_platform.py  # 🧹 Utilitários de limpeza
```

## 🚀 Getting Started

### Pré-requisitos

- **Python**: 3.11+
- **Poetry**: Gerenciamento de dependências
- **PostgreSQL**: Banco de dados (opcional para desenvolvimento)
- **Redis**: Cache e sessões (opcional)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/Aurora-AI/Aurora-Plataform.git
cd Aurora-Plataform

# Navegue para o Aurora-Core
cd aurora-core

# Instale dependências
poetry install

# Configure ambiente (copie e edite os arquivos de exemplo)
cp config/settings.example.toml config/settings.toml
cp config/.secrets.example.toml config/.secrets.toml
cp .env.example .env

# Execute migrações
poetry run alembic upgrade head

# Inicie o servidor
poetry run uvicorn src.aurora_platform.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000/docs`

## 🏗️ Componentes Principais

### Aurora-Core
**O Kernel do AIOS** - Orquestrador central responsável por:
- 🔄 **Roteamento Inteligente**: Distribuição eficiente de tarefas
- 🧠 **RAG Híbrido**: Sistema de memória ativa com ChromaDB
- 🔍 **DeepDive Scraper**: Camada de percepção web
- 🔐 **Segurança**: Autenticação JWT e validação robusta
- 📊 **Monitoramento**: Integração com Sentry e métricas

### Tecnologias

- **Backend**: FastAPI, SQLModel, Alembic
- **AI/ML**: ChromaDB, Google Gemini, Azure OpenAI
- **Infraestrutura**: Docker, Redis, PostgreSQL
- **DevOps**: GitHub Actions, Sentry, Poetry
- **Segurança**: JWT, bcrypt, rate limiting

## 🔧 Desenvolvimento

### Executar Testes

```bash
cd aurora-core
poetry run pytest
```

### Linting e Formatação

```bash
poetry run ruff check .
poetry run black .
```

### Estrutura de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(core): adiciona novo endpoint de autenticação
fix(api): corrige validação de tokens JWT
docs(readme): atualiza instruções de instalação
chore(deps): atualiza dependências do Poetry
```

## 📋 CI/CD

O projeto possui pipeline automatizado que executa:

- ✅ **Testes**: Suite completa com pytest
- 🔍 **Linting**: Verificação de código com Ruff
- 🏗️ **Build**: Validação de dependências
- 🚀 **Deploy**: Automação para ambientes

## 📖 Documentação

- **[Relatório Executivo](docs/reports/EXECUTIVE_REPORT_V2_ROLLOUT.md)**: Status e roadmap do projeto
- **[Checklists](docs/checklists/)**: Procedimentos operacionais
- **[Aurora-Core README](aurora-core/README.md)**: Documentação técnica detalhada

## 🤝 Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🏆 Status do Projeto

**Versão Atual**: v2.0 (Arquitetura Consolidada)  
**Status**: ✅ Produção  
**Última Atualização**: Dezembro 2024  

---

> **Aurora AI** - Construindo o futuro da Inteligência Artificial  
> 🌟 *"Where Intelligence Meets Innovation"*