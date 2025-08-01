# 🕷️ DeepDive Scraper Service - Fluxo Assíncrono

Serviço refatorado para implementar corretamente o fluxo assíncrono do Firecrawl.

## 📋 Funcionalidades Implementadas

### 1. Função `crawl_and_save()`
- **Fluxo Assíncrono Completo**: Implementa o padrão job-based do Firecrawl
- **Polling Inteligente**: Verifica status do job a cada 10 segundos
- **Tratamento de Estados**: Lida com 'pending', 'scraping', 'completed', 'failed'
- **Salvamento em Markdown**: Arquivos organizados com metadados

### 2. Estados do Job
- `pending` - Job na fila de processamento
- `scraping` - Crawling em andamento
- `completed` - Crawling concluído com sucesso
- `failed` - Erro durante o crawling

## 🚀 Como Usar

### Crawling Assíncrono
```python
# TODO: Reativar/substituir na integração do Crawler.
# from src.aurora_platform.services.deep_dive_scraper_service import crawl_and_save

# Crawling completo de um site
result = crawl_and_save("https://example.com", "data/crawled")
print(result)  # "Crawling concluído. X arquivos salvos em data/crawled"
```

### Scraping Simples (Página Única)
```python
# TODO: Reativar/substituir na integração do Crawler.
# from src.aurora_platform.services.deep_dive_scraper_service import scrape_url

# Scraping de uma página específica
data = await scrape_url("https://example.com")
```

## 🔄 Fluxo de Execução

1. **Inicialização**: `app.crawl_url()` retorna `job_id`
2. **Polling Loop**:
   - Chama `app.check_crawl_status(job_id)`
   - Verifica status retornado
   - Aguarda 10 segundos se ainda processando
3. **Finalização**:
   - Status 'completed' → Extrai dados e salva arquivos
   - Status 'failed' → Levanta exceção com erro

## 📁 Estrutura dos Arquivos Salvos

```
data/crawled/
├── crawled_a1b2c3d4_0.md    # Primeira página
├── crawled_e5f6g7h8_1.md    # Segunda página
└── ...
```

### Formato dos Arquivos Markdown
```markdown
# Título da Página

**URL:** https://example.com/page

---

Conteúdo extraído da página...
```

## ⚙️ Configuração

Configure a chave da API no `config/.secrets.toml`:
```toml
[default]
FIRECRAWL_API_KEY = "sua-chave-aqui"
```

## 🛠️ Tratamento de Erros

- **Job Failed**: Exceção com detalhes do erro
- **Timeout**: Loop infinito prevenido por estados válidos
- **API Key Inválida**: Erro 401 capturado e reportado
- **Sem Dados**: Exceção se nenhum conteúdo for extraído

## 📊 Logs de Acompanhamento

Durante o crawling, o serviço exibe:
```
Iniciando crawling de: https://example.com
Job ID: abc123
Status do job: pending... aguardando...
Status do job: scraping... aguardando...
Crawling concluído!
Salvo: data/crawled/crawled_a1b2c3d4_0.md
Crawling concluído. 3 arquivos salvos.
```

## 🔧 Melhorias de Robustez

### Validação de Configuração
- ✅ **Validador Pydantic**: `@field_validator` para `FIRECRAWL_API_KEY`
- ✅ **Limpeza Automática**: Remove espaços em branco com `strip()`
- ✅ **Validação de Nulidade**: Impede chaves vazias ou nulas

### Sistema de Logging
- ✅ **Logging Estruturado**: Substitui `print` por `logging`
- ✅ **Rastreabilidade**: Logs com timestamp e nível
- ✅ **Depuração**: Mostra primeiros caracteres da API key
- ✅ **Monitoramento**: Logs de status durante polling

### Diferenças da Versão Anterior
- ✅ **Antes**: `print` statements simples
- ✅ **Agora**: Sistema de logging profissional
- ✅ **Antes**: Sem validação de API key
- ✅ **Agora**: Validação robusta com Pydantic
- ✅ **Antes**: Tentativa de extração direta (falhava)
- ✅ **Agora**: Fluxo job-based correto com polling
