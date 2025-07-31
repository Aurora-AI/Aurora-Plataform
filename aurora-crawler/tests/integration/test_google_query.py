#!/usr/bin/env python3
import chromadb
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_google_query():
    try:
        # Conectar ao ChromaDB
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="aurora_knowledge")

        # Buscar especificamente documentos do Google
        google_docs = collection.get(
            where={"source": "https://ai.google.dev/gemini-api/docs?hl=pt-br"}
        )

        print(f"Documentos do Google encontrados: {len(google_docs['ids'])}")

        if google_docs["documents"]:
            print("\nConteúdo dos documentos do Google:")
            for i, doc in enumerate(google_docs["documents"]):
                print(f"\n--- Documento {i+1} ---")
                try:
                    clean_doc = doc.encode("ascii", "ignore").decode("ascii")
                    print(
                        clean_doc[:500] + "..." if len(clean_doc) > 500 else clean_doc
                    )
                except Exception as e:
                    print(f"Erro ao exibir documento: {e}")

        # Testar consultas específicas sobre Gemini
        queries = [
            "Gemini API",
            "modelo Gemini",
            "Google AI",
            "embedding model",
            "RAG retrieval",
        ]

        for query in queries:
            print(f"\n=== TESTE: {query} ===")
            results = collection.query(
                query_texts=[query],
                n_results=5,
                where={"source": "https://ai.google.dev/gemini-api/docs?hl=pt-br"},
            )

            docs = results.get("documents") if results is not None else None
            if docs and docs[0]:
                print(f"Resultados encontrados: {len(docs[0])}")
                for i, doc in enumerate(docs[0]):
                    try:
                        clean_doc = doc.encode("ascii", "ignore").decode("ascii")
                        print(f"\nResultado {i+1}: {clean_doc[:200]}...")
                    except Exception as e:
                        print(f"Erro: {e}")
            else:
                print("Nenhum resultado encontrado ou estrutura inválida.")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    test_google_query()
