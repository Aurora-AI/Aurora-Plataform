import requests
from bs4 import BeautifulSoup, Tag
from typing import Optional, List

url = "https://amb.org.br/category/noticias/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

print("=== ESTRUTURA DA PÁGINA ===")
# Procurar por diferentes seletores possíveis
selectors = [
    'a[href*="amb.org.br"]',
    ".post a",
    "article a",
    ".entry-title a",
    "h2 a",
    "h3 a",
    "h4 a",
    ".list-noticias a",
    "ul.list-noticias a",
    ".entry-content a",
]

for selector in selectors:
    links = soup.select(selector)
    if links:
        print(f'Seletor "{selector}" encontrou {len(links)} links:')
        for i, link in enumerate(links[:3]):  # Mostra apenas os 3 primeiros
            href = link.get("href", "N/A")
            text = link.get_text().strip()[:50]
            print(f'  {i+1}. {href} - "{text}"')
        print()

# Verificar a estrutura geral da página
print("=== ESTRUTURA GERAL ===")
main_content = soup.find("main") or soup.find("body")
if main_content and isinstance(main_content, Tag):
    # Procurar por artigos ou posts - usando seletor CSS mais direto
    articles = main_content.find_all(["article", "div"])
    # Filtrar manualmente os que têm classes relacionadas a posts
    post_articles = []
    for article in articles:
        if isinstance(article, Tag):
            css_classes = article.get("class")
            if css_classes:
                class_str = (
                    " ".join(css_classes)
                    if isinstance(css_classes, list)
                    else str(css_classes)
                )
                if any(
                    keyword in class_str for keyword in ["post", "entry", "noticia"]
                ):
                    post_articles.append(article)

    print(f"Encontrados {len(post_articles)} elementos de artigo/post")

    if post_articles:
        first_article = post_articles[0]
        if isinstance(first_article, Tag):
            article_classes = first_article.get("class")
            print(
                f"Primeiro artigo: {first_article.name} com classes: {article_classes}"
            )
            # Procurar links dentro do primeiro artigo
            article_links = first_article.find_all("a")
            print(f"Links no primeiro artigo: {len(article_links)}")
            for i, link in enumerate(article_links[:2]):
                if isinstance(link, Tag):
                    href = link.get("href", "N/A")
                    text = link.get_text().strip()[:30]
                    print(f'  Link {i+1}: {href} - "{text}"')
