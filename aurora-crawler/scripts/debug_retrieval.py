#!/usr/bin/env python3
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from aurora_platform.services.knowledge_service import KnowledgeBaseService


def debug_retrieval():
    try:
        # Inicializar serviço
        kb_service = KnowledgeBaseService()

        # Testar recuperação direta
        question = "Qual é o melhor modelo para trabalhos focados em RAG"

        print(f"Pergunta: {question}")
        print("=" * 50)

        # Recuperar documentos
        results = kb_service.retrieve(question, n_results=10)

        print(f"Documentos encontrados: {len(results['documents'][0])}")

        for i, (doc, meta) in enumerate(
            zip(results["documents"][0], results["metadatas"][0])
        ):
            print(f"\n--- Documento {i+1} ---")
            print(f"Fonte: {meta.get('source', 'N/A')}")
            print(f"Tipo: {meta.get('type', 'N/A')}")
            try:
                clean_doc = doc.encode("ascii", "ignore").decode("ascii")
                print(f"Conteúdo: {clean_doc[:200]}...")
            except Exception as e:
                print(f"Erro ao exibir: {e}")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    debug_retrieval()
