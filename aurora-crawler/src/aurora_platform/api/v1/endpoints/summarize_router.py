from fastapi import APIRouter, Depends, HTTPException, status, Request
from aurora_platform.schemas.knowledge_schemas import IngestURLRequest
from aurora_platform.services.rag_service import answer_query
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/summarize-url", status_code=status.HTTP_200_OK)
async def summarize_url_endpoint(request_body: IngestURLRequest):
    """
    Recebe uma URL, extrai o texto, gera resumo via RAG/LLM, persiste output por projeto.
    """
    try:
        url = request_body.url
        # Gera resumo usando pipeline RAG
        result = answer_query(url)
        # Persistir output em workspace/[project_name]/rag_output/summary.txt
        project_name = request_body.collection_name or "default_project"
        import os

        output_dir = f"workspace/{project_name}/rag_output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "summary.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["answer"])
        return {
            "status": "success",
            "output_path": output_path,
            "summary": result["answer"],
        }
    except Exception as e:
        logger.error(f"Erro ao resumir URL: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao resumir URL: {str(e)}")
