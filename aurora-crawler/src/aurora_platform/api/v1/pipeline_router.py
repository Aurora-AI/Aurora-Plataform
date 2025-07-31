from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from aurora_platform.services.pipeline_ingestion_service import PipelineIngestionService
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.core.project_manager import setup_project_workspace

router = APIRouter()


class PipelineRequest(BaseModel):
    project_name: str
    sources: List[Dict[str, Any]]
    actions: List[str] = []
    params: Dict[str, Any] = {}


@router.post("/api/v1/pipelines/execute")
async def execute_pipeline(request: PipelineRequest):
    ws = setup_project_workspace(request.project_name)
    kb_service = KnowledgeBaseService(persist_directory=ws["rag_output"])
    pipeline = PipelineIngestionService(kb_service)
    results = []
    from aurora_platform.services.semantic_analysis_service import (
        SemanticAnalysisService,
    )
    from aurora_platform.services.change_monitor_service import ChangeMonitorService
    from aurora_platform.api.v1.browser_router import summarize_url

    semantic_service = SemanticAnalysisService()
    change_monitor = ChangeMonitorService(scraper=pipeline.web_scraper, kb=kb_service)
    for action in request.actions:
        if action == "scrape":
            for source in request.sources:
                if source.get("source_type") == "url":
                    res = await pipeline.run_pipeline(
                        url=source["source_path"], collection_name=request.project_name
                    )
                    results.append({"scrape_result": res})
                elif source.get("source_type") == "file":
                    ids = pipeline.doc_processor.process_and_ingest_files(
                        [source["source_path"]], collection_name=request.project_name
                    )
                    results.append({"scrape_result": {"ingested_ids": ids}})
        elif action == "summarize_url":
            for source in request.sources:
                if source.get("source_type") == "url":
                    from aurora_platform.api.v1.browser_router import (
                        SummarizeUrlRequest,
                    )

                    req = SummarizeUrlRequest(
                        project_name=request.project_name,
                        url=source["source_path"],
                        params={},
                    )
                    res = await summarize_url(req)
                    results.append({"summarize_url_result": res})
        elif action == "semantic_analysis":
            for source in request.sources:
                if source.get("source_type") == "file":
                    with open(source["source_path"], "r", encoding="utf-8") as f:
                        text = f.read()
                    is_coherent = semantic_service.is_document_coherent(text)
                    results.append(
                        {
                            "semantic_analysis_result": {
                                "file": source["source_path"],
                                "is_coherent": is_coherent,
                            }
                        }
                    )
        elif action == "change_monitor":
            for source in request.sources:
                if source.get("source_type") == "url":
                    change_monitor.add_monitoring_task(
                        url=source["source_path"],
                        css_selector=request.params.get("css_selector", "body"),
                        interval=request.params.get("interval", 60),
                        collection=request.project_name,
                    )
                    results.append(
                        {
                            "change_monitor_result": f"Monitoring started for {source['source_path']}"
                        }
                    )
        # Adicione outros roteamentos de ação conforme necessário
    return {"workspace": ws, "results": results}
