# run_amb_scraper.py (v2 - Corrigido e Aprimorado)
import asyncio
import csv
from datetime import datetime
from typing import List, Dict, Optional, Union
import locale

import aiohttp
from bs4 import BeautifulSoup

# --- Configurações da Extração ---
BASE_URL = "https://amb.org.br/category/noticias/"
START_DATE = datetime(2019, 1, 1)
OUTPUT_FILE = "noticias_amb_desde_2019.csv"

# --- CORREÇÃO: Configura o locale para Português para extrair o mês corretamente ---
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    print("Aviso: Locale 'pt_BR.UTF-8' não suportado. Tentando 'Portuguese_Brazil'.")
    try:
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil")
    except locale.Error:
        print(
            "Aviso: Nenhum locale em Português suportado. A extração de datas pode falhar."
        )


async def fetch_page(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Busca o conteúdo HTML de uma URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        timeout = aiohttp.ClientTimeout(total=20)
        async with session.get(url, timeout=timeout, headers=headers) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Erro ao acessar {url}: {e}")
        return None


async def parse_article_page(
    session: aiohttp.ClientSession, article_url: str
) -> Union[Dict, str, None]:
    """Extrai os dados de uma única página de notícia."""
    html = await fetch_page(session, article_url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    try:
        # Buscar título - pode estar em diferentes locais
        title_tag = soup.find("h1") or soup.find("h2") or soup.find(".post-title")
        title = (
            title_tag.text.strip()
            if title_tag and title_tag.text.strip()
            else "Título não encontrado"
        )

        # Se o título ainda estiver vazio, tentar extrair do conteúdo
        if not title or title == "Título não encontrado":
            # Tentar encontrar o título na primeira linha do conteúdo
            content_div = soup.find("div", class_="entry-content")
            if content_div:
                first_line = content_div.get_text().split("\n")[0].strip()
                if first_line and len(first_line) > 10:
                    title = first_line[:100]

        # --- CORREÇÃO: Seletor de data ajustado ---
        date_tag = soup.find("time") or soup.find(class_="entry-date")
        date_str = date_tag.text.strip() if date_tag else ""

        # Converte a data para o formato datetime
        article_date = datetime.strptime(date_str.lower(), "%d de %B de %Y")

        # --- Filtro de Data ---
        if article_date < START_DATE:
            print(f"Notícia ignorada (antiga): {article_date.date()} - {title[:50]}...")
            return "STOP"  # Sinaliza para parar a paginação

        content_div = soup.find("div", class_="entry-content")
        full_text = (
            content_div.get_text(separator="\n", strip=True)
            if content_div
            else "Conteúdo não encontrado"
        )

        return {
            "titulo": title,
            "data_publicacao": article_date.strftime("%Y-%m-%d"),
            "link": article_url,
            "texto_completo": full_text,
        }
    except (AttributeError, ValueError, IndexError) as e:
        print(f"Erro ao processar a notícia {article_url}: {e}")
        return None


async def main():
    """Função principal para orquestrar o scraping."""
    all_news = []
    page_num = 1
    stop_pagination = False

    async with aiohttp.ClientSession() as session:
        while not stop_pagination:
            current_url = f"{BASE_URL}page/{page_num}/"
            print(f"Processando página de listagem: {current_url}")

            list_html = await fetch_page(session, current_url)
            if not list_html:
                break

            soup = BeautifulSoup(list_html, "html.parser")
            # --- CORREÇÃO: Seletor de links de notícias ajustado ---
            article_links = [
                str(a["href"])
                for a in soup.select(".post a")
                if a.get("href") and "noticias/" in str(a.get("href"))
            ]

            if not article_links:
                print("Nenhuma outra notícia encontrada na página. Finalizando.")
                break

            tasks = [parse_article_page(session, link) for link in article_links]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result == "STOP":
                    stop_pagination = True
                    break
                if isinstance(result, dict):
                    all_news.append(result)

            if stop_pagination:
                print(
                    "Data de corte atingida. Interrompendo a busca por páginas mais antigas."
                )
                break

            page_num += 1

    # --- Salvando os dados em CSV ---
    if all_news:
        print(f"\nExtração concluída. Total de {len(all_news)} notícias encontradas.")
        # Ordena as notícias da mais recente para a mais antiga antes de salvar
        all_news.sort(key=lambda x: x["data_publicacao"], reverse=True)
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["data_publicacao", "titulo", "link", "texto_completo"]
            )
            writer.writeheader()
            writer.writerows(all_news)
        print(f"Dados salvos com sucesso em: {OUTPUT_FILE}")
    else:
        print("Nenhuma notícia encontrada no período especificado.")


if __name__ == "__main__":
    asyncio.run(main())
