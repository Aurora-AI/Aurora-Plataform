#!/usr/bin/env python3
"""Script de teste para validar o scraper melhorado."""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# TODO: Reativar/substituir na integração do Crawler.
# from aurora_platform.services.deep_dive_scraper_service import DeepDiveScraperService


def test_scraper():
    """Testa o scraper com diferentes URLs."""

    # Mock Aurora para dependência externa do scraper
    class MockScraper:
        async def extract_text_from_url(self, url):
            return f"Conteúdo simulado para {url}"

    scraper = MockScraper()

    # URLs de teste
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://docs.trychroma.com/docs/overview/introduction",
    ]

    import asyncio

    for url in test_urls:
        print(f"\n--- Testando: {url} ---")
        try:
            content = asyncio.run(scraper.extract_text_from_url(url))
            print(f"[OK] Sucesso! Extraído {len(content)} caracteres")
            print(f"Prévia: {content[:200]}...")
        except Exception as e:
            print(f"[ERRO] {e}")


if __name__ == "__main__":
    test_scraper()
