#!/usr/bin/env python3
import chromadb
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def debug_chroma():
    try:
        # Conectar ao ChromaDB
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="aurora_knowledge")

        # Verificar quantos documentos existem
        count = collection.count()
        print(f"Total de documentos na coleção: {count}")

        if count > 0:
            # Buscar todos os documentos
            all_docs = collection.get()

            print(f"\nIDs dos documentos:")
            for i, doc_id in enumerate(all_docs["ids"]):
                print(f"{i+1}. {doc_id}")

            print(f"\nMetadados dos documentos:")
            for i, metadata in enumerate(all_docs["metadatas"]):
                print(f"{i+1}. {metadata}")

            # Mostrar uma amostra do conteúdo
            print(f"\nAmostra do conteúdo dos primeiros 3 documentos:")
            for i, doc in enumerate(all_docs["documents"][:3]):
                print(f"\nDocumento {i+1} (primeiros 200 caracteres):")
                try:
                    # Remover caracteres problemáticos
                    clean_doc = doc.encode("ascii", "ignore").decode("ascii")
                    print(
                        clean_doc[:200] + "..." if len(clean_doc) > 200 else clean_doc
                    )
                except Exception as e:
                    print(f"Erro ao exibir documento: {e}")

            # Testar uma consulta específica
            print(f"\n--- TESTE DE CONSULTA ---")
            query = "Qual é o melhor modelo para trabalhos focados em RAG"
            results = collection.query(query_texts=[query], n_results=3)

            print(f"Consulta: {query}")
            print(f"Documentos encontrados: {len(results['documents'][0])}")

            for i, doc in enumerate(results["documents"][0]):
                print(f"\nResultado {i+1} (primeiros 300 caracteres):")
                try:
                    clean_doc = doc.encode("ascii", "ignore").decode("ascii")
                    print(
                        clean_doc[:300] + "..." if len(clean_doc) > 300 else clean_doc
                    )
                except Exception as e:
                    print(f"Erro ao exibir resultado: {e}")
                print(f"Metadata: {results['metadatas'][0][i]}")
        else:
            print("Nenhum documento encontrado na coleção.")

    except Exception as e:
        print(f"Erro ao acessar ChromaDB: {e}")


if __name__ == "__main__":
    debug_chroma()
