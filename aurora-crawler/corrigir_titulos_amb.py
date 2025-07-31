import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import locale
from datetime import datetime
import re

# Configurar locale para português
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except:
    try:
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
    except:
        print("⚠️ Não foi possível configurar locale português, usando padrão")


def extrair_data_da_url(url):
    """Extrai data da URL da notícia"""
    # Padrão: /jornal-do-medico-19-07-2025
    match = re.search(r"jornal-do-medico-(\d{2})-(\d{2})-(\d{4})", url)
    if match:
        dia, mes, ano = match.groups()
        return f"{ano}-{mes}-{dia}"

    # Padrão alternativo: buscar qualquer data na URL
    match = re.search(r"(\d{2})-(\d{2})-(\d{4})", url)
    if match:
        dia, mes, ano = match.groups()
        return f"{ano}-{mes}-{dia}"

    # Se não conseguir extrair, usar data atual como fallback
    return datetime.now().strftime("%Y-%m-%d")


def extrair_titulo(soup, url):
    """Extrai título da notícia usando múltiplas estratégias"""
    # Estratégia 1: Segundo H1 (mais específico)
    h1_elements = soup.find_all("h1")
    if len(h1_elements) > 1:
        titulo = h1_elements[1].get_text(strip=True)
        if titulo:
            return titulo

    # Estratégia 2: Primeiro H1 não vazio
    for h1 in h1_elements:
        titulo = h1.get_text(strip=True)
        if titulo:
            return titulo

    # Estratégia 3: Title da página (removendo " – AMB")
    title_tag = soup.find("title")
    if title_tag:
        titulo_completo = title_tag.get_text(strip=True)
        # Remove " – AMB" do final
        titulo = titulo_completo.replace(" – AMB", "").strip()
        if titulo:
            return titulo

    # Estratégia 4: Tentar extrair do próprio URL
    if "jornal-do-medico" in url:
        partes = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
        # Converter hifens em espaços e capitalizar
        titulo_url = partes.replace("-", " ").replace("jornal do medico", "").strip()
        if titulo_url:
            return titulo_url.title()

    return "Título não encontrado"


async def extrair_conteudo_artigo(session, url):
    """Extrai o conteúdo completo de um artigo"""
    try:
        async with session.get(
            url, timeout=aiohttp.ClientTimeout(total=15)
        ) as response:
            if response.status != 200:
                return None, "Título não encontrado"

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Extrair título usando nova estratégia
            titulo = extrair_titulo(soup, url)

            # Remover scripts e estilos
            for script in soup(["script", "style"]):
                script.decompose()

            # Buscar o conteúdo principal
            seletores_conteudo = [
                "article",
                ".post-content",
                ".entry-content",
                ".content",
                "main",
                ".single-post",
            ]

            conteudo = ""
            for seletor in seletores_conteudo:
                elemento = soup.select_one(seletor)
                if elemento:
                    conteudo = elemento.get_text(separator="\n", strip=True)
                    break

            # Se não encontrou com seletores específicos, pega o body
            if not conteudo:
                body = soup.find("body")
                if body:
                    conteudo = body.get_text(separator="\n", strip=True)

            # Limpar e formatar o conteúdo
            linhas = [linha.strip() for linha in conteudo.split("\n") if linha.strip()]
            conteudo_limpo = "\n".join(linhas)

            return conteudo_limpo[:5000], titulo  # Limitar conteúdo a 5000 chars

    except Exception as e:
        print(f"❌ Erro ao processar {url}: {e}")
        return None, "Título não encontrado"


async def corrigir_csv_noticias():
    """Corrige o CSV existente com títulos corretos"""

    print("🔄 Iniciando correção de títulos do CSV de notícias da AMB...")

    # Ler CSV existente
    noticias_para_corrigir = []
    with open("noticias_amb_desde_2019.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            if linha["titulo"] == "Título não encontrado":
                noticias_para_corrigir.append(linha)

    print(f"📊 Total de notícias para corrigir títulos: {len(noticias_para_corrigir)}")

    # Processar em lotes menores para não sobrecarregar
    tamanho_lote = 50
    noticias_corrigidas = []

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(noticias_para_corrigir), tamanho_lote):
            lote = noticias_para_corrigir[i : i + tamanho_lote]
            print(
                f"🔄 Processando lote {i//tamanho_lote + 1}/{(len(noticias_para_corrigir) + tamanho_lote - 1)//tamanho_lote}..."
            )

            # Processar lote
            tasks = []
            for noticia in lote:
                tasks.append(extrair_conteudo_artigo(session, noticia["link"]))

            resultados = await asyncio.gather(*tasks, return_exceptions=True)

            # Processar resultados
            for j, resultado in enumerate(resultados):
                if isinstance(resultado, Exception):
                    print(f"❌ Erro: {resultado}")
                    continue

                if not isinstance(resultado, tuple) or len(resultado) != 2:
                    print(f"⚠️ Resultado inválido para índice {j}")
                    continue

                conteudo, titulo = resultado
                noticia_original = lote[j]

                # Atualizar dados
                noticia_corrigida = {
                    "data_publicacao": noticia_original["data_publicacao"],
                    "titulo": titulo,
                    "link": noticia_original["link"],
                    "texto_completo": (
                        conteudo if conteudo else noticia_original["texto_completo"]
                    ),
                }

                noticias_corrigidas.append(noticia_corrigida)

                # Mostrar progresso
                if titulo != "Título não encontrado":
                    print(f"✅ Título corrigido: {titulo[:80]}...")
                else:
                    print(
                        f"⚠️ Título ainda não encontrado para: {noticia_original['link']}"
                    )

            # Pausa entre lotes
            await asyncio.sleep(2)

    # Salvar CSV corrigido
    nome_arquivo = (
        f'noticias_amb_corrigidas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        campos = ["data_publicacao", "titulo", "link", "texto_completo"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(noticias_corrigidas)

    # Estatísticas finais
    titulos_corrigidos = sum(
        1 for n in noticias_corrigidas if n["titulo"] != "Título não encontrado"
    )

    print(f"\n📊 Correção Concluída!")
    print(f"✅ Títulos corrigidos: {titulos_corrigidos}/{len(noticias_corrigidas)}")
    print(f"💾 Arquivo salvo: {nome_arquivo}")
    print(f"📄 Tamanho: {len(noticias_corrigidas)} notícias")


if __name__ == "__main__":
    asyncio.run(corrigir_csv_noticias())
