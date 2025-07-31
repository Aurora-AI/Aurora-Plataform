# UNIFICATION_BLUEPRINT.md
## Diretriz AUR-UNIFY-001: Unificação dos Repositórios Aurora

### 📋 Ordem de Serviço Mestra

**Identificação:** AUR-UNIFY-001  
**Objetivo:** Migrar Aurora-Core e Aurora-Crawler para monorepo Aurora-Plataform  
**Status:** Em Execução  
**Data de Início:** $(date +'%Y-%m-%d')

### 🎯 Objetivos da Unificação

1. **Centralização do Código:** Consolidar todos os projetos Aurora em um único repositório
2. **Simplificação da Gestão:** Reduzir complexidade de versionamento e deploy
3. **Facilitação da Colaboração:** Melhorar visibilidade entre equipes
4. **Padronização:** Estabelecer práticas consistentes em todos os módulos
5. **Orquestração Unificada:** Deploy e gerenciamento centralizados

### 🏗️ Estrutura de Migração

#### Antes da Unificação:
```
Repositórios Separados:
├── Aurora-AI/Aurora-Core       (Backend/API)
├── Aurora-AI/Aurora-Crawler    (Web Scraping)
└── Aurora-AI/Aurora-Frontend   (Interface - Futuro)
```

#### Após a Unificação:
```
Aurora-Plataform/ (Monorepo)
├── aurora-core/              # Ex: Aurora-Core
├── aurora-crawler/           # Ex: Aurora-Crawler  
├── aurora-frontend/          # Ex: Aurora-Frontend (Futuro)
├── docs/                     # Documentação centralizada
├── scripts/                  # Utilitários compartilhados
├── docker-compose.yaml       # Orquestração unificada
└── README.md                 # Documentação principal
```

### ✅ Checklist de Migração

#### Fase 1: Preparação (CONCLUÍDA)
- [x] Criação do repositório Aurora-Plataform
- [x] Definição da estrutura de diretórios
- [x] Planejamento da estratégia de migração

#### Fase 2: Migração do Código (CONCLUÍDA)
- [x] Migração do Aurora-Core para aurora-core/
- [x] Migração do Aurora-Crawler para aurora-crawler/
- [x] Remoção de diretórios .git dos subprojetos
- [x] Preservação do histórico via submodules (se necessário)

#### Fase 3: Infraestrutura Unificada (EM EXECUÇÃO)
- [x] Criação do README.md principal
- [x] Criação da estrutura docs/
- [ ] Criação dos scripts/ utilitários
- [ ] Configuração do docker-compose.yaml principal
- [ ] Limpeza de configurações duplicadas

#### Fase 4: Documentação e Finalização
- [x] Criação do UNIFICATION_BLUEPRINT.md
- [ ] Atualização das documentações individuais
- [ ] Criação de guias de desenvolvimento
- [ ] Testes de integração end-to-end

### 🔧 Configurações Removidas/Consolidadas

#### Arquivos Removidos dos Subprojetos:
- `.git/` directories (mantido apenas no root)
- Docker Compose duplicados (consolidados no root)
- Configurações de CI/CD conflitantes

#### Arquivos Mantidos nos Subprojetos:
- `pyproject.toml` (dependências específicas)
- `.env.example` (configurações específicas)
- `README.md` (documentação técnica específica)
- Dockerfiles individuais

### 🚀 Benefícios Esperados

1. **Deploy Simplificado:** Um único comando para subir toda a plataforma
2. **Desenvolvimento Facilitado:** Setup mais simples para novos desenvolvedores
3. **Versionamento Unificado:** Releases coordenados entre componentes
4. **Documentação Centralizada:** Visão holística da arquitetura
5. **CI/CD Otimizado:** Pipelines coordenados e eficientes

### 🔐 Considerações de Segurança

- Separação de segredos por ambiente (.env por módulo)
- Permissões de acesso granulares mantidas
- Logs e auditoria centralizados
- Isolamento de containers preservado

### 📊 Métricas de Sucesso

- [ ] Tempo de setup reduzido em 70%
- [ ] Complexidade de deploy reduzida
- [ ] Melhor colaboração entre equipes
- [ ] Documentação mais acessível
- [ ] Redução de bugs de integração

### 🎯 Próximos Passos

1. **Automação:** Scripts de setup e deploy
2. **Monitoring:** Observabilidade unificada
3. **Testing:** Suíte de testes integrados
4. **Documentation:** Portal de documentação
5. **Expansion:** Integração de novos módulos

### 📞 Contatos e Responsáveis

**Coordenador da Migração:** Aurora AI Team  
**Revisão Técnica:** Arquitetos de Software  
**Aprovação Final:** Tech Lead

---

**Documento Criado em:** $(date +'%Y-%m-%d %H:%M:%S')  
**Versão:** 1.0  
**Status:** Documento Vivo (Atualizado conforme progresso)