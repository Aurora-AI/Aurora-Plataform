# Aurora Agent Packager

Este agente automatiza o processo de adição de dependências à Plataforma Aurora, sob rígidas regras de governança e segurança.

## Visão Geral

O Aurora Agent Packager é um sistema de automação que gerencia dependências na Plataforma Aurora, garantindo que apenas pacotes aprovados e seguros sejam introduzidos nos projetos.

## Fluxo de Trabalho

### 1. Solicitação de Nova Dependência

1. **Trigger:** Issue com label `new-dependency`
2. **Formato da Issue:** 
   ```
   Título: [DEPENDENCY] Nome do Pacote
   Corpo: 
   package: nome-do-pacote
   versão: ^1.0.0
   justificativa: Descrição da necessidade
   ```

### 2. Processo de Validação

1. **Extração:** Nome do pacote extraído automaticamente do corpo da issue
2. **Validação:** Verifica se o pacote está em `approved_packages.json`
   - **Se APROVADO:** Adiciona comentário de confirmação
   - **Se NÃO APROVADO:** Adiciona label `security-review-required` e solicita revisão
3. **Notificação:** Core team (@aurora-dev/core-team) é mencionado automaticamente

### 3. Verificação em Pull Requests

- **Detecção:** Monitora modificações em `pyproject.toml` e arquivos de dependências
- **Alertas:** Adiciona comentários informativos sobre verificações necessárias
- **Controle:** Nenhum PR é mesclado automaticamente; revisão humana obrigatória

## Configuração

### Arquivo de Configuração: `approved_packages.json`

```json
{
  "version": "1.0.0",
  "last_updated": "2024-01-31",
  "description": "Lista de pacotes aprovados para uso na Plataforma Aurora",
  "approved_packages": [
    "fastapi",
    "pydantic",
    "sqlmodel"
  ],
  "sources": {
    "aurora-core": ["fastapi", "pydantic"],
    "aurora-crawler": ["sqlmodel", "beautifulsoup4"]
  }
}
```

### Atualização da Allowlist

Para adicionar um novo pacote à lista de aprovados:

1. Edite `approved_packages.json`
2. Adicione o pacote à lista `approved_packages`
3. Atualize a seção `sources` correspondente
4. Atualize `last_updated` com a data atual
5. Crie um PR com a mudança

## Critérios de Segurança

### Pacotes Aprovados Devem:

- ✅ Ter licença compatível (MIT, Apache 2.0, BSD)
- ✅ Ser mantidos ativamente (última atualização < 6 meses)
- ✅ Ter boa reputação na comunidade
- ✅ Não ter vulnerabilidades conhecidas
- ✅ Seguir princípio de menor privilégio

### Pacotes Rejeitados:

- ❌ Licenças restritivas (GPL, AGPL)
- ❌ Pacotes descontinuados ou abandonados
- ❌ Dependências com vulnerabilidades críticas
- ❌ Pacotes com funcionalidades desnecessárias

## Labels Utilizadas

- `new-dependency`: Solicitação de nova dependência
- `security-review-required`: Requer revisão de segurança
- `dependency-approved`: Dependência aprovada pelo time
- `dependency-rejected`: Dependência rejeitada

## Workflow GitHub Actions

O agente opera através do arquivo `.github/workflows/aurora-agent-packager.yml`:

- **Triggers:** Issues e Pull Requests
- **Verificações:** Validação automática contra allowlist
- **Notificações:** Comentários automáticos e menções ao core team
- **Segurança:** Nenhuma mesclagem automática

## Responsabilidades do Core Team

1. **Revisão de Segurança:** Avaliar pacotes não aprovados
2. **Atualização da Allowlist:** Manter `approved_packages.json` atualizado
3. **Aprovação Final:** Revisar e aprovar todos os PRs manualmente
4. **Monitoramento:** Acompanhar vulnerabilidades em dependências aprovadas

## Exemplo de Uso

### Issue para Nova Dependência

```markdown
# [DEPENDENCY] requests-oauth

package: requests-oauth
versão: ^2.1.0
justificativa: Necessário para autenticação OAuth2 no módulo de integração

## Contexto
Este pacote será usado para implementar autenticação OAuth2 com APIs externas...
```

### Resposta Automática

```markdown
⚠️ **Revisão de Segurança Necessária**: `requests-oauth` não está na lista de pacotes aprovados.

Este pacote requer revisão de segurança antes da inclusão. A label `security-review-required` foi adicionada.

@aurora-dev/core-team favor revisar este pacote.
```

## Conformidade e Auditoria

- Todos os pacotes são rastreados em `approved_packages.json`
- Histórico de aprovações mantido via Git
- Logs de verificação disponíveis nos Actions do GitHub
- Processo transparente e auditável

---

**Versão:** 1.0.0  
**Última Atualização:** 2024-01-31  
**Responsável:** Aurora Platform Core Team