import asyncio
from src.aurora_platform.services.scraper_service import DeepDiveScraperServiceV2


async def test_scraper():
    service = DeepDiveScraperServiceV2()
    # Teste com uma página real
    await service.deep_dive_scrape("https://www.gov.br/pt-br/noticias")
    print("Teste de extração finalizado. Verifique output.md e output_rag.json.")

    # Teste de resiliência (Circuit Breaker)
    try:
        for i in range(7):  # Força falhas para abrir o breaker
            await service.deep_dive_scrape("https://httpstat.us/500")
    except Exception as e:
        print(f"Circuit Breaker ativado: {e}")


if __name__ == "__main__":
    asyncio.run(test_scraper())
