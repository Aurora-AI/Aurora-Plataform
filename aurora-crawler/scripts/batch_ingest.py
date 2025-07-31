import os
import argparse
import sys
import logging

# Adiciona o diretório 'src' ao path para que possamos importar nossos módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main(directory_path: str):
    """
    Função principal que varre um diretório, processa os arquivos suportados
    e os ingere na base de conhecimento.
    """
    if not os.path.isdir(directory_path):
        logger.error(f"O caminho fornecido não é um diretório válido: {directory_path}")
        return

    logger.info("Inicializando serviços para ingestão em lote...")
    try:
        # Inicializa os serviços necessários
        kb_service = KnowledgeBaseService()
        doc_processor = DocumentProcessingService(kb_service)

        # Lista os arquivos a serem processados
        files_to_process = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]

        if not files_to_process:
            logger.warning(f"Nenhum arquivo encontrado no diretório: {directory_path}")
            return

        logger.info(f"Iniciando o processamento de {len(files_to_process)} arquivos...")

        # Chama o serviço de processamento com a lista de arquivos
        ingested_ids = doc_processor.process_and_ingest_files(files_to_process)

        logger.info("--- Resumo da Ingestão em Lote ---")
        logger.info(f"Total de arquivos encontrados: {len(files_to_process)}")
        logger.info(f"Total de documentos ingeridos com sucesso: {len(ingested_ids)}")
        logger.info(f"IDs dos documentos ingeridos: {ingested_ids}")
        logger.info("------------------------------------")

    except Exception as e:
        logger.exception(f"Ocorreu um erro crítico durante a ingestão em lote: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script para ingestão em lote de documentos para a Memória Ativa da Aurora."
    )
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        default=r"C:\Users\winha\Aurora\data\Base RJ",
        help="O caminho para o diretório contendo os documentos a serem ingeridos. (Padrão: Base RJ)",
    )
    args = parser.parse_args()

    main(args.directory)
