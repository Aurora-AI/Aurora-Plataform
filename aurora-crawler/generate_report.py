# generate_report.py
import pandas as pd
from datetime import datetime

INPUT_FILE = "noticias_amb_corrigidas_20250723_164612.csv"
OUTPUT_FILE = f"noticias_amb_relatorio_{datetime.now().strftime('%Y%m%d')}.md"


def classify_topic(title: str, text: str) -> str:
    """
    Classifica uma notícia em um tópico com base em palavras-chave.

    NOTA DE ARQUITETURA: Este é o ponto de integração para um LLM/SLM.
    Em um fluxo de produção, o título e o texto seriam enviados a um modelo
    de linguagem para uma classificação semântica muito mais precisa.
    """
    title_lower = title.lower()
    text_lower = text.lower()

    # Regras de classificação, da mais específica para a mais geral
    if any(keyword in title_lower for keyword in ["congresso", "cmg 2025"]):
        return "Congresso AMB"
    if any(
        keyword in text_lower
        for keyword in [
            "frente parlamentar",
            "ministério da saúde",
            "ans",
            "cfm",
            "deputado",
            "senador",
        ]
    ):
        return "Política e Regulamentação Médica"
    if any(
        keyword in text_lower for keyword in ["sociedade brasileira de", "sbp", "sboc"]
    ):
        return "Relações com Sociedades de Especialidade"
    if any(
        keyword in title_lower
        for keyword in ["saúde pública", "pandemia", "covid-19", "vacina"]
    ):
        return "Saúde Pública"
    if any(keyword in title_lower for keyword in ["evento", "simpósio", "webinar"]):
        return "Eventos Científicos"
    if "amb" in title_lower:
        return "Notícias da Entidade"

    return "Outros Tópicos"


def generate_report():
    """
    Lê o arquivo de dados, classifica, agrupa e gera o relatório final em Markdown.
    """
    try:
        # --- 1. Extração e Organização ---
        print(f"Lendo dados de '{INPUT_FILE}'...")
        # O arquivo parece ser separado por vírgula
        df = pd.read_csv(INPUT_FILE)
        # Garante que os nomes das colunas estão limpos
        df.columns = [col.strip() for col in df.columns]

        # Limpeza e conversão de dados
        df = df.dropna(subset=["titulo", "texto_completo"])
        df["data_publicacao"] = pd.to_datetime(df["data_publicacao"])

        print("Classificando notícias por tópico...")
        df["topico"] = df.apply(
            lambda row: classify_topic(row["titulo"], row["texto_completo"]), axis=1
        )

        # Ordena o DataFrame inteiro pela data, da mais recente para a mais antiga
        df = df.sort_values(by="data_publicacao", ascending=False)

        print(
            f"Notícias classificadas nos seguintes tópicos: {df['topico'].unique().tolist()}"
        )

        # --- 2. Formatação do Documento ---
        print("Gerando o documento Markdown...")
        report_content = []

        # Agrupa por tópico para a geração do relatório
        grouped = df.groupby("topico")

        # Cria o Sumário
        report_content.append(
            "# Relatório de Notícias da Associação Médica Brasileira\n"
        )
        report_content.append("## Sumário\n")
        chapter_num = 1
        topic_list = sorted(df["topico"].unique())
        for topic in topic_list:
            report_content.append(f"{chapter_num}. {topic}")
            chapter_num += 1
        report_content.append("\n---\n")

        # Cria os Capítulos
        chapter_num = 1
        for topic in topic_list:
            report_content.append(f"# Capítulo {chapter_num}: {topic}\n")

            topic_df = grouped.get_group(topic)

            for index, row in topic_df.iterrows():
                report_content.append(
                    f"## {row['data_publicacao'].strftime('%d de %B de %Y')}"
                )
                report_content.append(f"### {row['titulo']}")
                report_content.append(
                    f"[Link para a notícia original]({row['link']})\n"
                )
                report_content.append(f"{row['texto_completo']}\n")
                report_content.append("---\n")

            chapter_num += 1

        # --- 3. Exportação ---
        final_report = "\n".join(report_content)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final_report)

        # --- 4. Entrega ---
        print(f"\n✅ Missão concluída com sucesso!")
        print(f"O relatório foi gerado e salvo em: '{OUTPUT_FILE}'")

    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo de entrada '{INPUT_FILE}' não foi encontrado.")
    except Exception as e:
        print(f"❌ ERRO: Ocorreu um erro inesperado durante o processamento: {e}")


if __name__ == "__main__":
    generate_report()
