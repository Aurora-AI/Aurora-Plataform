# Copilot Instructions for Aurora-Crawler

## Visão Geral da Arquitetura
- O projeto é uma POC de um sistema de ingestão, processamento e indexação de documentos e URLs, com integração a uma base de conhecimento (KnowledgeBaseService).
- O código principal está em `src/aurora_platform/` e subdiretórios, com serviços, APIs, schemas e lógica de ingestão.
- O fluxo típico: arquivos/URLs são processados por `DocumentProcessingService`, que extrai texto e envia para a base de conhecimento.
- O diretório `scripts/` contém utilitários de ingestão em lote.
- Testes estão em `tests/` e arquivos de teste na raiz.

## Convenções e Padrões
- Serviços seguem o padrão de injeção de dependências (ex: `DocumentProcessingService` recebe `KnowledgeBaseService`).
- Processamento de arquivos suporta `.pdf` (via PyMuPDF/fitz) e `.docx` (python-docx). URLs são processadas com requests + BeautifulSoup.
- Após processar arquivos, eles são removidos do disco.
- IDs de documentos seguem o padrão: `file_<nome>` para arquivos, `url_<hash>` para URLs.
- Logs são feitos via o módulo `logging`.

## Workflows de Desenvolvimento
- Instale dependências com `install_dependencies.bat` ou via Poetry (`pyproject.toml`).
- Para rodar testes: utilize `pytest` (há arquivos de teste tanto em `tests/` quanto na raiz).
- Scripts utilitários: `start_chroma_server.bat` (inicia o banco ChromaDB), `start_dev_mode.bat` (modo dev), `install_and_test.bat` (instala e testa).
- O banco ChromaDB é usado para persistência e está em `chroma_db/`.

## Integrações e Pontos Críticos
- Integração principal é com ChromaDB (persistência) e serviços de scraping/processamento de documentos.
- O serviço de conhecimento (`KnowledgeBaseService`) é central para ingestão e indexação.
- O processamento de URLs remove scripts/estilos antes de extrair texto.

## Exemplos de Uso
- Para ingerir múltiplas fontes:
  - Use `DocumentProcessingService.process_and_ingest_sources(sources)` onde `sources` é uma lista de dicts com `source_type` ('file' ou 'url') e `source_path`.
- Para adicionar um novo tipo de documento, adicione um método `_extract_text_from_<tipo>` e atualize o roteamento em `process_and_ingest_files`.

## Observações
- Siga os padrões de logging e tratamento de erros já presentes.
- Não deixe arquivos temporários após processamento.
- Consulte os scripts `.bat` para comandos de build/dev/test específicos do projeto.
