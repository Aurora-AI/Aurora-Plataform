# Aurora Platform CI/CD - Configuração de Proteção de Branch

## Configuração Necessária para Branch Protection

Para implementar a proteção da branch `main` conforme especificado no plano técnico AUR-PLATFORM-CI-002, siga estas instruções:

### 1. Configuração via Interface GitHub

1. Acesse as configurações do repositório Aurora-Plataform
2. Navegue até "Settings" > "Branches"
3. Clique em "Add branch protection rule"
4. Configure as seguintes opções:

**Branch name pattern:** `main`

**Configurações obrigatórias:**
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

**Status checks obrigatórios:**
- `test-core`
- `test-crawler`

**Configurações adicionais recomendadas:**
- ✅ Require pull request reviews before merging (mínimo 1 reviewer)
- ✅ Dismiss stale PR approvals when new commits are pushed
- ✅ Require review from code owners (se aplicável)
- ✅ Restrict pushes that create files larger than 100 MB

### 2. Verificação da Configuração

Após aplicar as configurações:
1. Tente fazer merge de um PR sem que os checks `test-core` e `test-crawler` tenham passado
2. Confirme que o GitHub bloqueia o merge
3. Verifique que apenas PRs com todos os status checks aprovados podem ser mesclados

### 3. Comandos GitHub CLI (Alternativa)

```bash
# Configurar proteção via GitHub CLI
gh api repos/Aurora-AI/Aurora-Plataform/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test-core","test-crawler"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null
```

## Notas Importantes

- Esta configuração garante que todas as alterações na branch `main` passem pelos testes automatizados
- Os jobs `test-core` e `test-crawler` devem completar com sucesso antes do merge
- A configuração protege contra regressions e mantém a qualidade do código