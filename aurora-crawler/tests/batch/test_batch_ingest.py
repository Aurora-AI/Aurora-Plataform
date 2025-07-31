import subprocess
import sys
import os


def test_batch_ingest():
    """Testa o script de ingestão em lote"""
    print("🚀 TESTANDO INGESTÃO EM LOTE\n")

    # Caminho para o script
    script_path = os.path.join("scripts", "batch_ingest.py")
    directory_path = "documentos_para_ingestao"

    try:
        print(f"📁 Executando: python {script_path} {directory_path}")
        print("=" * 50)

        # Executa o script
        result = subprocess.run(
            [sys.executable, script_path, directory_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )

        # Mostra a saída
        if result.stdout:
            print("📋 SAÍDA:")
            print(result.stdout)

        if result.stderr:
            print("⚠️ ERROS:")
            print(result.stderr)

        print("=" * 50)
        print(f"🎯 Código de saída: {result.returncode}")

        if result.returncode == 0:
            print("✅ INGESTÃO EM LOTE CONCLUÍDA COM SUCESSO!")
        else:
            print("❌ INGESTÃO EM LOTE FALHOU!")

    except Exception as e:
        print(f"❌ Erro ao executar o script: {e}")


if __name__ == "__main__":
    test_batch_ingest()
