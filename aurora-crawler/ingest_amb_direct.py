#!/usr/bin/env python3
"""
Script para ingestão direta das notícias da AMB no ChromaDB
"""
import chromadb
import csv
import uuid
from datetime import datetime
from typing import List, Dict


def ingest_amb_news_to_chroma():
    """Ingere as notícias da AMB diretamente no ChromaDB"""

    print("🚀 Iniciando ingestão das notícias da AMB no ChromaDB...")

    # Conectar ao ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="amb_noticias")

    # Ler as notícias do CSV corrigido
    noticias = []
    with open(
        "noticias_amb_corrigidas_20250723_164612.csv", "r", encoding="utf-8"
    ) as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            if linha["titulo"] and linha["titulo"] != "Título não encontrado":
                noticias.append(linha)

    print(f"📊 Total de notícias para ingerir: {len(noticias)}")

    # Preparar dados para ingestão em lotes
    batch_size = 100
    total_ingested = 0

    for i in range(0, len(noticias), batch_size):
        batch = noticias[i : i + batch_size]

        # Preparar documentos do lote
        ids = []
        documents = []
        metadatas = []

        for noticia in batch:
            # Criar ID único
            noticia_id = f"amb_{uuid.uuid4().hex[:8]}"
            ids.append(noticia_id)

            # Preparar conteúdo do documento
            conteudo = f"""Título: {noticia['titulo']}

Data de Publicação: {noticia['data_publicacao']}

Conteúdo:
{noticia['texto_completo']}

Fonte: Associação Médica Brasileira (AMB)
Link: {noticia['link']}"""

            documents.append(conteudo)

            # Preparar metadados
            metadata = {
                "source": "AMB",
                "title": noticia["titulo"],
                "publication_date": noticia["data_publicacao"],
                "link": noticia["link"],
                "type": "news_article",
                "ingested_at": datetime.now().isoformat(),
            }
            metadatas.append(metadata)

        try:
            # Ingerir lote no ChromaDB
            collection.add(ids=ids, documents=documents, metadatas=metadatas)

            total_ingested += len(batch)
            lote_atual = (i // batch_size) + 1
            total_lotes = (len(noticias) + batch_size - 1) // batch_size

            print(
                f"✅ Lote {lote_atual}/{total_lotes} processado - {len(batch)} notícias ingeridas"
            )

        except Exception as e:
            lote_atual = (i // batch_size) + 1
            print(f"❌ Erro ao ingerir lote {lote_atual}: {e}")
            continue

    # Verificar resultado final
    total_count = collection.count()
    print(f"\n📊 Ingestão Concluída!")
    print(f"✅ Notícias processadas: {total_ingested}/{len(noticias)}")
    print(f"📚 Total de documentos na coleção: {total_count}")

    # Testar uma consulta
    print(f"\n🔍 Testando consulta na base de conhecimento...")
    test_query = "residência médica"
    results = collection.query(query_texts=[test_query], n_results=3)

    print(f"Consulta: '{test_query}'")

    try:
        if (
            results
            and "documents" in results
            and results["documents"]
            and results["documents"][0]
        ):
            docs = results["documents"][0]
            print(f"Resultados encontrados: {len(docs)}")

            # Tentar extrair metadados se disponíveis
            metadatas = []
            if (
                "metadatas" in results
                and results["metadatas"]
                and results["metadatas"][0]
            ):
                metadatas = results["metadatas"][0]

            for i, doc in enumerate(docs):
                metadata = metadatas[i] if i < len(metadatas) else {}
                print(f"\nResultado {i+1}:")
                print(f"  Título: {metadata.get('title', 'N/A')}")
                print(f"  Data: {metadata.get('publication_date', 'N/A')}")
                print(f"  Trecho: {doc[:200]}...")
        else:
            print("Nenhum resultado encontrado para a consulta teste.")
    except Exception as e:
        print(f"Erro ao processar resultados da consulta: {e}")

    return total_count


if __name__ == "__main__":
    try:
        total_docs = ingest_amb_news_to_chroma()
        print(
            f"\n🎉 Sucesso! {total_docs} documentos disponíveis na base de conhecimento AMB."
        )
    except Exception as e:
        print(f"❌ Erro durante a ingestão: {e}")
        import traceback

        traceback.print_exc()
