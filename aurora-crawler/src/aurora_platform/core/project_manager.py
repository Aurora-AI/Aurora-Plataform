import os
from pathlib import Path


def setup_project_workspace(project_name: str) -> dict:
    """
    Cria diretórios de workspace para o projeto informado.
    Estrutura: raw/, processed/, rag_output/, logs/
    Retorna dict com caminhos absolutos criados.
    """
    base_dir = Path(f"projects/{project_name}").absolute()
    dirs = {
        "raw": base_dir / "raw",
        "processed": base_dir / "processed",
        "rag_output": base_dir / "rag_output",
        "logs": base_dir / "logs",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return {k: str(v) for k, v in dirs.items()}


# Exemplo de uso:
if __name__ == "__main__":
    ws = setup_project_workspace("amb_noticias")
    print(ws)
