import logging
from .scraper_service import DeepDiveScraperServiceV2
from .document_processing_service import DocumentProcessingService
from .knowledge_service import KnowledgeBaseService
from typing import List

logger = logging.getLogger(__name__)


class PipelineIngestionService:
    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service
        self.doc_processor = DocumentProcessingService(self.kb_service)
        self.web_scraper = DeepDiveScraperServiceV2()

    async def run_pipeline(
        self, url: str, collection_name: str = "default_knowledge_base"
    ) -> dict:
        logger.info(f"Pipeline de ingestão iniciado para a URL: {url}")
        downloaded_files = await self.web_scraper.download_pdfs_from_url(url)
        if not downloaded_files:
            logger.warning(f"Nenhum documento para download encontrado na URL: {url}")
            return {
                "message": "Nenhum documento suportado encontrado para ingestão.",
                "total_ingested": 0,
            }
        ingested_ids = []
        for file_path in downloaded_files:
            if file_path.endswith((".xlsx", ".xls")):
                documents = self.doc_processor.extract_text_from_excel(file_path)
                self.kb_service.add_documents(list(documents), collection_name)
                ingested_ids.append(file_path)
            elif file_path.endswith(".pdf"):
                text = self.doc_processor.extract_text_from_pdf(file_path)
                self.kb_service.add_document(file_path, text, {}, collection_name)
                ingested_ids.append(file_path)
            # ... outros formatos ...
        summary = {
            "message": "Pipeline de ingestão concluído.",
            "total_downloaded": len(downloaded_files),
            "total_ingested": len(ingested_ids),
            "ingested_document_ids": ingested_ids,
        }
        logger.info(summary)
        return summary
