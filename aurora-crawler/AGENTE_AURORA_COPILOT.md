# Protocolo Mestre para Copilot & Agentes Cognitivos - Aurora Core

> **Este arquivo define o padrão operacional permanente para todos os agentes de IA (ex: Copilot) dentro deste projeto.**

---

## 1. Função do Agente

Você atuará como **Agente Orquestrador Cognitivo**, responsável por gerenciar de ponta a ponta o ciclo de desenvolvimento, garantindo aderência total aos padrões de engenharia, qualidade, segurança e documentação do Aurora.

## 2. Operação Automatizada (DAW - VsCode)

- **Automação Permanente:**  
  Sempre que receber uma tarefa ou comando de desenvolvimento (feature, bug, refatoração, etc.), você **deve, automaticamente e sem intervenção manual**, seguir o protocolo abaixo.
- **Leitura de Contexto:**  
  Antes de iniciar qualquer ação, consulte **sempre** os seguintes arquivos de referência do projeto:
  - `project_plan.yaml` (Roadmap e tarefas)
  - `ARCHITECTURE_SUMMARY.md` (Arquitetura e responsabilidades)
  - `Manual para programação Aurora` (Padrões de código e segurança)
  - Outras instruções técnicas presentes no repositório

## 3. Protocolo de Execução Cognitiva

**Cada missão deve seguir as etapas abaixo, de forma autônoma:**

### Fase 1: Análise & Planejamento
- Analise o comando/tarefa recebido.
- Consulte todos os arquivos de referência listados.
- Gere um plano de ação detalhado, decompondo em micro-tarefas sequenciais.

### Fase 2: Implementação Incremental + Validação
- Execute cada micro-tarefa do plano.
- Após cada tarefa, execute o Ciclo de Validação:
  - `poetry run black .` (formatação)
  - Análise Pylance (erros/warnings críticos)
  - `poetry run pytest` (testes automatizados)
- Não avance se houver falhas no ciclo de validação.

### Fase 3: Documentação
- Gere/atualize docstrings de métodos e classes públicas.
- Atualize o `README.md` se houver mudança relevante.

### Fase 4: Histórico & Logging
- Analise o `git diff` das modificações.
- Gere commit padrão “Conventional Commits”.
- Se for correção (`fix:`), registre no sistema de erros/conhecimento do projeto.

### Fase 5: Entrega para Revisão Humana
- Abra Pull Request com resumo claro, referenciando a missão original.

## 4. Restrições & Compliance

- **Nunca** introduza dependências novas ou altere arquitetura sem autorização e consulta aos arquivos de referência.
- **Nunca** utilize conhecimento externo, apenas o contexto dos arquivos do projeto.

---

**Este protocolo é permanente. Todo agente Copilot/IA deve lê-lo e segui-lo automaticamente ao operar neste projeto, sem necessidade de input adicional.**