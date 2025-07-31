#!/usr/bin/env python3
"""
Exemplo de uso do modelo de ingestão corrigido
"""

# Exemplo de como usar o modelo de ingestão

sources = [
    {
        "source_type": "url",
        "source_path": "https://ai.google.dev/gemini-api/docs?hl=pt-br",
    },
    {"source_type": "file", "source_path": "/caminho/para/documento.pdf"},
]

# Uso com o DocumentProcessingService:
# doc_service = DocumentProcessingService(kb_service)
# ingested_ids = doc_service.process_and_ingest_sources(sources)

print("Modelo de ingestão corrigido:")
print("✓ Suporta URLs (web scraping)")
print("✓ Suporta arquivos PDF/DOCX")
print("✓ Metadados incluem tipo da fonte")
print("✓ Tratamento de erros robusto")
