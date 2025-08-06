#!/usr/bin/env python3
# run_dashboard.py
import subprocess
import sys
from pathlib import Path


def run_dashboard():
    """Executa o dashboard Streamlit."""
    dashboard_path = Path(__file__).parent / "dashboard.py"

    try:
        print("ğŸš€ Iniciando Aurora Project Dashboard...")
        print("ğŸ“Š Acesse: http://localhost:8501")
        print("â�¹ï¸�  Para parar: Ctrl+C")
        print("-" * 50)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_path),
                "--server.port=8501",
                "--server.address=localhost",
            ]
        )

    except KeyboardInterrupt:
        print("\nâœ… Dashboard encerrado.")
    except Exception as e:
        print(f"â�Œ Erro ao executar dashboard: {e}")


if __name__ == "__main__":
    run_dashboard()
