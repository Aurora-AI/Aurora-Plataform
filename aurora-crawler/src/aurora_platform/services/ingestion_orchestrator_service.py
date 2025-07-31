import logging
import aiohttp
from bs4 import BeautifulSoup
from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2
from .document_processing_service import DocumentProcessingService
from .knowledge_service import KnowledgeBaseService

logger = logging.getLogger(__name__)


class IngestionOrchestratorService:
    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service
        self.doc_processor = DocumentProcessingService(kb_service)
        self.web_scraper = DeepDiveScraperServiceV2()

    async def process_ingestion(
        self, source_type: str, source_path: str, collection_name: str
    ):
        logger.info(
            f"Orquestrador de ingestão iniciado para a fonte: {source_type} - {source_path}"
        )

        if source_type == "url":
            # Tentar primeiro baixar documentos
            # Substituir crawl_and_download_files pelo método público correto
            if hasattr(self.web_scraper, "download_pdfs_from_url"):
                downloaded_files = await self.web_scraper.download_pdfs_from_url(
                    source_path
                )
            else:
                downloaded_files = []
            if downloaded_files:
                # Se encontrou documentos, processa eles
                ingested_ids = self.doc_processor.process_and_ingest_files(
                    downloaded_files, collection_name=collection_name
                )
                return {
                    "ingested_ids": ingested_ids,
                    "source": source_path,
                    "type": "documents",
                }
            else:
                # Se não encontrou documentos, faz scraping do HTML
                return await self._ingest_html_content(source_path)

        elif source_type == "file_upload":
            # A lógica para lidar com uploads de arquivos diretos viria aqui
            # (usando o DocumentProcessingService)
            raise NotImplementedError(
                "A ingestão via 'file_upload' ainda não foi implementada."
            )

        else:
            raise ValueError(f"Tipo de fonte de ingestão desconhecido: '{source_type}'")

    async def _ingest_html_content(self, url: str):
        """Ingere conteúdo HTML diretamente"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Remove scripts e styles
                    for script in soup(["script", "style"]):
                        script.decompose()

                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (
                        phrase.strip() for line in lines for phrase in line.split("  ")
                    )
                    text = " ".join(chunk for chunk in chunks if chunk)

                    # Fragmentar texto em chunks menores
                    chunk_size = 1000
                    chunks = [
                        text[i : i + chunk_size]
                        for i in range(0, len(text), chunk_size)
                    ]

                    ingested_ids = []
                    for i, chunk in enumerate(chunks):
                        if len(chunk.strip()) > 50:  # Só adiciona chunks com conteúdo
                            doc_id = f"web_{hash(url)}_{i}"
                            metadata = {"source": url, "chunk": i, "type": "web"}
                            self.kb_service.add_document(
                                document_id=doc_id,
                                text=chunk,
                                metadata=metadata,
                                collection_name="default_knowledge_base",
                            )
                            ingested_ids.append(doc_id)

                    return {
                        "ingested_ids": ingested_ids,
                        "source": url,
                        "type": "html",
                        "chunks_added": len(ingested_ids),
                    }
        except Exception as e:
            logger.error(f"Erro ao ingerir HTML: {e}")
            raise ValueError(f"Falha ao processar conteúdo HTML da URL: {url}")
