# src/aurora_platform/dependencies.py
from fastapi import Request

from aurora_platform.services.knowledge_service import KnowledgeService


def get_kb_service(request: Request) -> KnowledgeService:
    return request.app.state.kb_service
