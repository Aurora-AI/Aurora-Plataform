# ...imports...


# Imports principais e definição do router devem vir antes dos endpoints
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from aurora_platform.schemas.knowledge_schemas import (
    KnowledgeQuery,
    SearchResult,
    IngestionRequest,
    IngestURLRequest,
)
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.api.v1.endpoints.auth_router import get_current_user
import os
import tempfile
import logging
from aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)
from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2

logger = logging.getLogger(__name__)

router = APIRouter()


def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service


# Imports principais e definição do router devem vir antes dos endpoints
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from aurora_platform.schemas.knowledge_schemas import (
    KnowledgeQuery,
    SearchResult,
    IngestionRequest,
    IngestURLRequest,
)
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.api.v1.endpoints.auth_router import get_current_user
import os
import tempfile
import logging
from aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)
from src.aurora_platform.services.scraper_service import DeepDiveScraperServiceV2

logger = logging.getLogger(__name__)

router = APIRouter()


# Novo endpoint para deep crawl e ingestão de documentos encontrados em um domínio
@router.post("/ingest-deep-crawl", status_code=status.HTTP_202_ACCEPTED)
async def run_deep_crawl_ingestion(
    request_body: IngestURLRequest,
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Inicia um 'deep crawl' em uma URL para encontrar, baixar, processar
    e ingerir todos os documentos suportados.
    """
    try:
        scraper = DeepDiveScraperServiceV2()
        file_paths = await scraper.download_pdfs_from_url(request_body.url)

        if not file_paths:
            raise HTTPException(
                status_code=404,
                detail="Nenhum documento suportado (.pdf, .docx) encontrado para download.",
            )

        processor = DocumentProcessingService(kb_service)
        ingested_ids = processor.process_and_ingest_files(
            file_paths, collection_name=request_body.collection_name
        )

        return {
            "message": "Processo de deep crawl e ingestão concluído.",
            "total_downloaded": len(file_paths),
            "total_ingested": len(ingested_ids),
            "ingested_document_ids": ingested_ids,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro durante o processo de ingestão: {str(e)}"
        )


from aurora_platform.services.knowledge_query_service import KnowledgeQueryService
from aurora_platform.services.ingestion_orchestrator_service import (
    IngestionOrchestratorService,
)


# Novo endpoint de ingestão de arquivo local
@router.post("/knowledge/ingest-from-file", status_code=status.HTTP_200_OK)
async def ingest_from_file(
    file: UploadFile = File(...),
    params: IngestionRequest = Depends(),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
    current_user: str = Depends(get_current_user),
):
    """
    Endpoint para upload e ingestão de arquivos locais (PDF, DOCX).
    Protegido por autenticação JWT.
    """
    filename = str(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        # Delega a extração e ingestão para o serviço
        processor = DocumentProcessingService(kb_service)
        processor.process_and_ingest_files(
            [tmp_path], collection_name=params.collection_name
        )
        os.remove(tmp_path)
        return {"message": f"Arquivo '{filename}' ingerido com sucesso."}
    except Exception as e:
        logger.error(f"Erro ao ingerir arquivo {filename}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}"
        )


@router.post("/ingestions", status_code=status.HTTP_202_ACCEPTED)
async def create_ingestion_task(
    request_body: IngestionRequest,
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Endpoint único para iniciar todas as tarefas de ingestão de conhecimento.
    """
    try:
        orchestrator = IngestionOrchestratorService(kb_service)
        result = await orchestrator.process_ingestion(
            source_type=request_body.source_type,
            source_path=request_body.source_path,
            collection_name=request_body.collection_name,
        )
        return {"message": "Tarefa de ingestão concluída.", "details": result}
    except NotImplementedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro inesperado durante a ingestão: {str(e)}"
        )


@router.post("/search", response_model=SearchResult)
async def search_in_kb(query: KnowledgeQuery):
    from aurora_platform.services.knowledge_service import KnowledgeBaseService

    kb_service = KnowledgeBaseService()
    docs = kb_service.retrieve(query=query.query, n_results=query.n_results)
    contents = [
        (
            doc["page_content"]
            if isinstance(doc, dict) and "page_content" in doc
            else str(doc)
        )
        for doc in docs
    ]
    return SearchResult(results=contents)


@router.post("/ask")
async def ask(
    query: KnowledgeQuery, kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """Endpoint RAG com Chain-of-Thought"""
    query_service = KnowledgeQueryService(kb_service)
    return query_service.answer_query(query.query, query.n_results)
