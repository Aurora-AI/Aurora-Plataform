import os
import sys

# Adiciona o diretório 'src' ao path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Ingere documentos da Base RJ"""
    directory_path = r"C:\Users\winha\Aurora\data\Base RJ"

    if not os.path.isdir(directory_path):
        logger.error(f"Diretório não encontrado: {directory_path}")
        return

    logger.info("🚀 INICIANDO INGESTÃO DA BASE RJ")
    logger.info(f"📁 Diretório: {directory_path}")

    try:
        # Inicializa serviços
        kb_service = KnowledgeBaseService()
        doc_processor = DocumentProcessingService(kb_service)

        # Lista arquivos
        files_to_process = []
        for f in os.listdir(directory_path):
            file_path = os.path.join(directory_path, f)
            if os.path.isfile(file_path):
                files_to_process.append(file_path)

        if not files_to_process:
            logger.warning("❌ Nenhum arquivo encontrado!")
            return

        logger.info(f"📋 Encontrados {len(files_to_process)} arquivos")

        # Lista os arquivos que serão processados
        for i, file_path in enumerate(files_to_process, 1):
            filename = os.path.basename(file_path)
            logger.info(f"  {i}. {filename}")

        # Processa arquivos
        logger.info("⚙️ Iniciando processamento...")
        ingested_ids = doc_processor.process_and_ingest_files(files_to_process.copy())

        # Resumo
        logger.info("=" * 50)
        logger.info("📊 RESUMO DA INGESTÃO")
        logger.info(f"📁 Diretório: Base RJ")
        logger.info(f"📄 Arquivos encontrados: {len(files_to_process)}")
        logger.info(f"✅ Documentos ingeridos: {len(ingested_ids)}")
        logger.info(f"📋 IDs: {ingested_ids}")
        logger.info("=" * 50)
        logger.info("🎉 INGESTÃO CONCLUÍDA COM SUCESSO!")

    except Exception as e:
        logger.exception(f"❌ Erro crítico: {e}")


if __name__ == "__main__":
    main()
