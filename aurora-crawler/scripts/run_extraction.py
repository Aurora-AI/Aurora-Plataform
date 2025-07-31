import asyncio
import argparse
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / "src"))

from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2
from aurora_platform.services.knowledge_service import KnowledgeBaseService


async def main(url: str, output_path: str):
    """
    Orquestra a extração de conteúdo de uma URL e salva em um arquivo.
    """
    print(f"Iniciando extração da URL: {url}")

    kb_service = KnowledgeBaseService()
    scraper = DeepDiveScraperServiceV2()

    try:
        # Ajuste o nome do método conforme a implementação real do serviço
        extracted_content = await scraper.deep_dive_scrape(url)

        if extracted_content:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Fonte: {url}\n\n")
                f.write(extracted_content)
            print(f"✅ Conteúdo salvo com sucesso em: {output_path}")
        else:
            print(f"⚠️ Não foi possível extrair conteúdo da URL: {url}")

    except Exception as e:
        print(f"❌ Erro fatal durante a extração de {url}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrator de Conhecimento da Aurora.")
    parser.add_argument("--url", required=True, help="URL da página a ser extraída.")
    parser.add_argument(
        "--output", required=True, help="Caminho do arquivo de saída .md."
    )
    args = parser.parse_args()

    asyncio.run(main(args.url, args.output))
