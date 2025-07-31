#!/usr/bin/env python3
import chromadb
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def clean_and_test():
    try:
        # Conectar ao ChromaDB
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="aurora_knowledge")

        # Buscar todos os documentos
        all_docs = collection.get()

        print(f"Total de documentos antes da limpeza: {len(all_docs['ids'])}")

        # Identificar documentos para remover (manter apenas os do Google)
        ids_to_remove = []
        for i, metadata in enumerate(all_docs["metadatas"]):
            source = metadata.get("source", "")
            if "ai.google.dev" not in source:
                ids_to_remove.append(all_docs["ids"][i])

        print(f"Documentos a serem removidos: {len(ids_to_remove)}")

        # Remover documentos antigos
        if ids_to_remove:
            collection.delete(ids=ids_to_remove)
            print("Documentos removidos com sucesso!")

        # Verificar o que restou
        remaining_docs = collection.get()
        print(f"Documentos restantes: {len(remaining_docs['ids'])}")

        # Testar consulta
        if remaining_docs["ids"]:
            print("\n=== TESTE DE CONSULTA ===")
            query = "Qual é o melhor modelo para trabalhos focados em RAG"
            results = collection.query(query_texts=[query], n_results=3)

            print(f"Consulta: {query}")
            print(f"Resultados encontrados: {len(results['documents'][0])}")

            for i, (doc, meta) in enumerate(
                zip(results["documents"][0], results["metadatas"][0])
            ):
                print(f"\n--- Resultado {i+1} ---")
                print(f"Fonte: {meta.get('source', 'N/A')}")
                try:
                    clean_doc = doc.encode("ascii", "ignore").decode("ascii")
                    print(f"Conteúdo: {clean_doc[:300]}...")
                except Exception as e:
                    print(f"Erro: {e}")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    clean_and_test()
