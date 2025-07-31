from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from aurora_platform.schemas.knowledge_schemas import IngestURLRequest
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.services.pipeline_ingestion_service import PipelineIngestionService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service


@router.post("/ingest-documents-from-url", status_code=status.HTTP_202_ACCEPTED)
async def run_ingestion_pipeline(
    request_body: IngestURLRequest,
    background_tasks: BackgroundTasks,
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Inicia a tarefa de ingestão completa de documentos de uma URL em segundo plano.
    """
    try:
        orchestrator = PipelineIngestionService(kb_service)
        # Adiciona a execução do pipeline como uma tarefa de fundo
        background_tasks.add_task(
            orchestrator.run_pipeline,
            url=request_body.url,
            collection_name=request_body.collection_name,
        )

        return {
            "message": "Processo de ingestão iniciado. Os documentos serão processados em segundo plano."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao iniciar o pipeline de ingestão: {str(e)}"
        )


@router.post("/ingest-deep-crawl-from-url", status_code=status.HTTP_202_ACCEPTED)
async def run_deep_crawl_pipeline(
    request_body: IngestURLRequest,
    background_tasks: BackgroundTasks,
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Inicia a tarefa de deep crawl e ingestão de um site inteiro em segundo plano.
    """

    async def pipeline_task():
        logger.info(f"Pipeline de deep crawl iniciado para a URL: {request_body.url}")
        scraper = PipelineIngestionService(kb_service).web_scraper
        downloaded_files = await scraper.download_pdfs_from_url(request_body.url)

        for file_path in downloaded_files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                doc_id = f"web_{hash(file_path)}_{len(text)}"
                metadata = {"source": file_path, "type": "deep_crawl"}
                kb_service.add_document(
                    document_id=doc_id,
                    text=text,
                    metadata=metadata,
                    collection_name=request_body.collection_name,
                )
            except Exception as e:
                logger.error(f"Erro ao processar arquivo {file_path}: {e}")

        logger.info(f"Ingestão de {len(downloaded_files)} arquivos concluída.")

    background_tasks.add_task(pipeline_task)
    return {"message": "Processo de deep crawl e ingestão iniciado em segundo plano."}
