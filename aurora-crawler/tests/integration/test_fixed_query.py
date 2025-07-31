#!/usr/bin/env python3
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.services.knowledge_query_service import KnowledgeQueryService


def test_fixed_query():
    try:
        # Inicializar serviços
        kb_service = KnowledgeBaseService()
        query_service = KnowledgeQueryService(kb_service)

        # Testar a pergunta original
        question = "Qual é o melhor modelo para trabalhos focados em RAG"

        print(f"Pergunta: {question}")
        print("=" * 50)

        result = query_service.answer_query(question, n_results=3)

        print(f"Resposta: {result['answer']}")
        print(f"\nCadeia de Pensamento: {result['chain_of_thought']}")
        print(f"\nFontes utilizadas: {result['sources']}")

        if "context_used" in result:
            print(
                f"\nContexto utilizado (primeiros 300 chars): {result['context_used'][:300]}..."
            )

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    test_fixed_query()
