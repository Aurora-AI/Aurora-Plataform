import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def debug_titulo():
    # Testando com uma URL específica do CSV
    url = "https://amb.org.br/noticias/jornal-do-medico-19-07-2025-3o-congresso-de-medicina-geral-da-amb-contara-com-a-participacao-de-mais-de-300-palestrantes-renomados-de-todas-as-especialidades-da-medicina/"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Testando diferentes seletores para título
                seletores_teste = [
                    "h1",
                    "h1.entry-title",
                    ".entry-title",
                    "h1.post-title",
                    ".post-title",
                    "h2.entry-title",
                    "title",
                    ".article-title",
                    ".news-title",
                    ".page-title",
                ]

                print(f"URL: {url}")
                print("=" * 80)

                for seletor in seletores_teste:
                    elemento = soup.select_one(seletor)
                    if elemento:
                        titulo = elemento.get_text(strip=True)
                        print(f"✅ {seletor}: '{titulo}'")
                    else:
                        print(f"❌ {seletor}: Não encontrado")

                # Vamos também ver o title da página
                title_tag = soup.find("title")
                if title_tag:
                    print(f"\n🏷️ Title da página: '{title_tag.get_text(strip=True)}'")

                # Vamos procurar por todos os H1s
                all_h1 = soup.find_all("h1")
                if all_h1:
                    print(f"\n📋 Todos os H1s encontrados:")
                    for i, h1 in enumerate(all_h1):
                        print(f"  {i+1}. '{h1.get_text(strip=True)}'")

        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")


if __name__ == "__main__":
    asyncio.run(debug_titulo())
