# Script de Ingestão em Lote - Aurora-Core

## 📋 Descrição
Script para ingestão em massa de documentos na "Memória Ativa" do Aurora-Core.

## 🚀 Como Usar

### 1. Preparar Documentos
```bash
# Criar diretório (já existe)
mkdir documentos_para_ingestao

# Adicionar seus arquivos (.pdf, .docx, .txt)
# Exemplo: copiar arquivos para documentos_para_ingestao/
```

### 2. Executar Ingestão
```bash
# Método 1: Direto
python scripts/batch_ingest.py documentos_para_ingestao

# Método 2: Teste automatizado
python test_batch_ingest.py
```

## 📁 Estrutura
```
Aurora-Core/
├── scripts/
│   └── batch_ingest.py          # Script principal
├── documentos_para_ingestao/    # Diretório de entrada
│   ├── exemplo.txt              # Arquivo de teste 1
│   └── exemplo2.txt             # Arquivo de teste 2
└── test_batch_ingest.py         # Script de teste
```

## ✅ Formatos Suportados
- `.pdf` - Documentos PDF
- `.docx` - Documentos Word
- `.txt` - Arquivos de texto

## 📊 Saída Esperada
```
2025-07-14 12:00:00 - INFO - Inicializando serviços para ingestão em lote...
2025-07-14 12:00:01 - INFO - Iniciando o processamento de 2 arquivos...
2025-07-14 12:00:02 - INFO - --- Resumo da Ingestão em Lote ---
2025-07-14 12:00:02 - INFO - Total de arquivos encontrados: 2
2025-07-14 12:00:02 - INFO - Total de documentos ingeridos com sucesso: 2
2025-07-14 12:00:02 - INFO - IDs dos documentos ingeridos: ['file_exemplo.txt', 'file_exemplo2.txt']
2025-07-14 12:00:02 - INFO - ------------------------------------
```

## 🔧 Requisitos
- Servidor Aurora-Core rodando
- ChromaDB inicializado
- Arquivos no diretório especificado