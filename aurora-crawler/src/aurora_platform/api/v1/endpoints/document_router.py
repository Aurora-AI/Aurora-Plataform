from fastapi import APIRouter, Depends, UploadFile, File, Request, HTTPException
from fastapi.responses import JSONResponse
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService
from src.aurora_platform.services.document_processing_service import (
    DocumentProcessingService,
)
from src.aurora_platform.schemas.document_schemas import DocumentIngestRequest
from typing import List
import os
import tempfile
import shutil
from pydantic import BaseModel, ValidationError


class SourceItem(BaseModel):
    source_type: str
    source_path: str


class ProcessSourcesRequest(BaseModel):
    sources: List[SourceItem]


router = APIRouter(prefix="/documents", tags=["Document Ingestion"])


def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service


@router.post("/ingest-files")
async def ingest_files(
    files: List[UploadFile] = File(...),
    params: DocumentIngestRequest = Depends(),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Recebe um ou mais arquivos (PDF, DOCX), extrai o texto e ingere
    na base de conhecimento na coleção especificada.
    """
    if not files:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado.")

    processor = DocumentProcessingService(kb_service)
    temp_dir = tempfile.mkdtemp(prefix="aurora_uploads_")
    temp_paths = []

    try:
        for file in files:
            if file.filename:
                temp_path = os.path.join(temp_dir, file.filename)
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                temp_paths.append(temp_path)

        # Passa o nome da coleção para o serviço
        ingested_ids = []
        for path in temp_paths:
            filename = os.path.basename(path)
            text = ""
            if filename.lower().endswith(".pdf"):
                text = processor.extract_text_from_pdf(path)
            elif filename.lower().endswith((".docx", ".doc")):
                text = processor.extract_text_from_docx(path)
            else:
                continue
            if text.strip():
                doc_id = f"file_{filename}"
                metadata = {"source": f"local_upload_{filename}"}
                kb_service.add_document(
                    doc_id, text, metadata, collection_name=params.collection_name
                )
                ingested_ids.append(doc_id)

        return {
            "message": f"{len(ingested_ids)} de {len(files)} arquivos foram ingeridos com sucesso.",
            "ingested_ids": ingested_ids,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ocorreu um erro no processamento: {str(e)}"
        )
    finally:
        # Garante a limpeza do diretório temporário e seus conteúdos
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@router.post("/process-and-ingest")
async def process_and_ingest(
    file: UploadFile = File(...),
    params: DocumentIngestRequest = Depends(),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """Processar documento e ingerir na base de conhecimento"""
    if not file or not getattr(file, "filename", None):
        raise HTTPException(status_code=400, detail="Nome do arquivo é obrigatório")

    supported_formats = [".pdf", ".docx", ".doc"]
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Nome do arquivo é obrigatório")
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado. Formatos aceitos: {', '.join(supported_formats)}",
        )

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        service = DocumentProcessingService(kb_service)

        if file_ext == ".pdf":
            pages = service.extract_text_from_pdf(temp_path)
            extracted_text = "\n".join(pages)
        elif file_ext in [".docx", ".doc"]:
            extracted_text = service.extract_text_from_docx(temp_path)
        else:
            extracted_text = ""

        if not extracted_text.strip():
            raise HTTPException(
                status_code=422, detail="Não foi possível extrair texto do documento"
            )

        doc_id = f"doc_{file.filename}_{hash(extracted_text) % 10000}"
        doc_metadata = {
            "source": "document_upload",
            "filename": file.filename,
            "type": "document_processing",
        }

        kb_service.add_document(
            doc_id, extracted_text, doc_metadata, collection_name=params.collection_name
        )

        return JSONResponse(
            content={
                "status": "success",
                "document_id": doc_id,
                "ingested": True,
                "filename": file.filename,
                "text_length": len(extracted_text),
            }
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/process-and-ingest-multiple")
async def process_and_ingest_multiple(
    files: list[UploadFile] = File(...),
    params: DocumentIngestRequest = Depends(),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """Processar múltiplos documentos e ingerir na base de conhecimento"""
    results = []

    for file in files:
        if not file or not getattr(file, "filename", None):
            continue
        if file.filename and file.filename.lower().endswith(".pdf"):
            file_ext = ".pdf"
        elif file.filename and file.filename.lower().endswith(".docx"):
            file_ext = ".docx"
        elif file.filename and file.filename.lower().endswith(".doc"):
            file_ext = ".doc"
        else:
            continue
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=file_ext
            ) as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_path = temp_file.name
            service = DocumentProcessingService(kb_service)
            if file_ext == ".pdf":
                pages = service.extract_text_from_pdf(temp_path)
                extracted_text = "\n".join(pages)
            elif file_ext in [".docx", ".doc"]:
                extracted_text = service.extract_text_from_docx(temp_path)
            else:
                extracted_text = ""
            if extracted_text.strip():
                doc_id = f"doc_{file.filename}_{hash(extracted_text) % 10000}"
                doc_metadata = {
                    "source": "multiple_upload",
                    "filename": file.filename,
                    "type": "document_processing",
                }
                kb_service.add_document(
                    doc_id,
                    extracted_text,
                    doc_metadata,
                    collection_name=params.collection_name,
                )
                results.append(
                    {"filename": file.filename, "status": "success", "doc_id": doc_id}
                )
            else:
                results.append(
                    {
                        "filename": file.filename,
                        "status": "failed",
                        "error": "No text extracted",
                    }
                )
        except Exception as e:
            results.append(
                {"filename": file.filename, "status": "failed", "error": str(e)}
            )

    successful = len([r for r in results if r["status"] == "success"])

    return {
        "total_files": len(files),
        "successful": successful,
        "failed": len(files) - successful,
        "results": results,
    }


@router.post("/process-sources")
async def process_sources(
    request: ProcessSourcesRequest,
    params: DocumentIngestRequest = Depends(),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """Processar múltiplas fontes (URLs e arquivos) e ingerir na base de conhecimento"""
    try:
        service = DocumentProcessingService(kb_service)
        sources_data = [
            {"source_type": source.source_type, "source_path": source.source_path}
            for source in request.sources
        ]
        ingested_ids = (
            service.process_and_ingest_sources(
                sources_data, collection_name=params.collection_name
            )
            or []
        )
        return JSONResponse(
            content={
                "status": "success",
                "total_sources": len(request.sources),
                "ingested_count": len(ingested_ids),
                "ingested_ids": ingested_ids,
            }
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Erro de validação: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
