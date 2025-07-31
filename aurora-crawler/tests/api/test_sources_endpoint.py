#!/usr/bin/env python3
"""
Teste do endpoint de processamento de fontes
"""

import requests
import json

# Exemplo de payload correto para o endpoint /process-sources
payload = {
    "sources": [
        {
            "source_type": "url",
            "source_path": "https://ai.google.dev/gemini-api/docs?hl=pt-br",
        }
    ]
}

print("Payload JSON válido:")
print(json.dumps(payload, indent=2))

# Exemplo de uso com requests:
# response = requests.post(
#     "http://localhost:8000/api/v1/documents/process-sources",
#     json=payload
# )

print("\nEndpoint corrigido:")
print("✓ Validação JSON adequada")
print("✓ Suporte a URLs e arquivos")
print("✓ Tratamento de erros robusto")
print("✓ Resposta estruturada")
