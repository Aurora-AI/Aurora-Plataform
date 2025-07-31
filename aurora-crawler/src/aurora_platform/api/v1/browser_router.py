from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any
from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2
from aurora_platform.core.project_manager import setup_project_workspace
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class SummarizeUrlRequest(BaseModel):
    project_name: str
    url: str
    params: Dict[str, Any] = {}


@router.post("/browser/summarize-url")
async def summarize_url(request: SummarizeUrlRequest):
    ws = setup_project_workspace(request.project_name)
    scraper = DeepDiveScraperServiceV2()
    html = await scraper.fetch_page(request.url)
    # Salva HTML bruto no workspace
    from pathlib import Path

    raw_path = Path(ws["raw"]) / "summarized_url.html"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(html)
    # Simula resumo (em produção, integrar modelo de sumarização)
    summary = f"Resumo do conteúdo de {request.url}: ..."
    summary_path = Path(ws["processed"]) / "summarized_url.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    logger.info(f"Resumo salvo em {summary_path}")
    return {
        "status": "success",
        "project_name": request.project_name,
        "workspace_path": str(ws),
        "outputs": {"raw_html": str(raw_path), "summary": str(summary_path)},
    }
