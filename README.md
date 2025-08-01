# Aurora-Core: Núcleo Minimalista de Orquestração RAG

## 1. Visão do Projeto


O **Aurora-Core** é o Kernel Cognitivo do ecossistema Aurora: um orquestrador minimalista, responsável apenas pelo pipeline RAG (Retrieval-Augmented Generation), seus adapters, fábricas e testes essenciais. Todo o restante é considerado legado e não faz parte deste repositório.


**Doutrina:**
- O Core só orquestra o pipeline RAG (Qdrant, adapters, factories, ingestão e consulta).
- Nenhum serviço, API, modelo ou teste fora desse escopo é mantido aqui.
- Para autenticação, usuários, scraping, automações etc., utilize repositórios satélites.


## 2. Arquitetura Técnica (Minimalista)

- **Linguagem:** Python 3.11+
- **Gerenciamento de Dependências:** Poetry
- **Vector Store:** Qdrant (local/cloud)
- **Testes:** Pytest


## 3. Núcleo Mantido

- `knowledge_service.py` (+ `.pyi`)
- `knowledge_ingestion_service.py`
- `rag_service.py`
- `adapter_factory.py`
- `llm_adapters.py`
- `qdrant_adapter.py`
- (Opcional: `llm_phi3_adapter.py`)


## 4. Como Usar

1.  **Instale as dependências:**
    ```bash
    poetry install
    ```
2.  **Configure o ambiente:**
    - Copie o arquivo `config/settings.example.toml` para `config/settings.toml`.
    - Configure as variáveis de ambiente do Qdrant (`QDRANT_URL`, `QDRANT_API_KEY` se cloud).
3.  **Execute os testes:**
    ```bash
    poetry run pytest
    ```

---

> O Aurora-Core não implementa autenticação, scraping, automações, APIs REST ou qualquer serviço além do pipeline RAG. Para essas funções, utilize os repositórios satélites.

# Aurora-Core: Trigger manual do workflow após migração
