import requests
from bs4 import BeautifulSoup

URL = "https://docs.agno.com/introduction"
OUTPUT_MD = "introduction.md"


def fetch_and_save_markdown(url: str, output_path: str):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts e estilos
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Extrai o texto principal
    text = soup.get_text(separator="\n", strip=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Arquivo salvo: {output_path}")


if __name__ == "__main__":
    fetch_and_save_markdown(URL, OUTPUT_MD)
