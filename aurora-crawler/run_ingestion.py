# run_ingestion.py
import csv
import httpx
import asyncio

# --- Configurações da Ingestão ---
API_BASE_URL = (
    "http://localhost:8001"  # Ajuste se a porta do seu contêiner for diferente
)
INGEST_ENDPOINT = "/api/v1/pipelines/ingest-document"
CSV_FILE_PATH = "noticias_amb_corrigidas_20250723_164612.csv"
COLLECTION_NAME = "amb_noticias"  # Nome da coleção dedicada a este conhecimento


async def ingest_article(client: httpx.AsyncClient, article: dict):
    """Envia um único artigo para o endpoint de ingestão."""
    payload = {
        "text_content": f"Título: {article['titulo']}\n\n{article['texto_completo']}",
        "collection_name": COLLECTION_NAME,
        "metadata": {
            "source_link": article["link"],
            "publication_date": article["data_publicacao"],
            "original_title": article["titulo"],
        },
    }
    try:
        response = await client.post(INGEST_ENDPOINT, json=payload, timeout=60.0)
        response.raise_for_status()
        print(f"✅ Sucesso ao ingerir: {article['titulo'][:50]}...")
        return True
    except httpx.HTTPStatusError as e:
        print(
            f"❌ Falha ao ingerir: {article['titulo'][:50]}... | Status: {e.response.status_code} | Resposta: {e.response.text}"
        )
        return False
    except httpx.RequestError as e:
        print(f"❌ Erro de conexão ao ingerir: {article['titulo'][:50]}... | Erro: {e}")
        return False


async def main():
    """Lê o CSV e orquestra a ingestão de todos os artigos."""
    articles_to_ingest = []
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles_to_ingest.append(row)

    print(
        f"Total de {len(articles_to_ingest)} notícias para ingerir na coleção '{COLLECTION_NAME}'."
    )

    successful_ingestions = 0
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        tasks = [ingest_article(client, article) for article in articles_to_ingest]
        results = await asyncio.gather(*tasks)
        successful_ingestions = sum(1 for r in results if r)

    print("\n--- Processo de Ingestão Concluído ---")
    print(
        f"Total de Ingestões Bem-sucedidas: {successful_ingestions}/{len(articles_to_ingest)}"
    )


if __name__ == "__main__":
    # Garanta que seu contêiner Docker com a API esteja rodando antes de executar
    asyncio.run(main())
