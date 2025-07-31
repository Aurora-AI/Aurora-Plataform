from pydantic import BaseModel
from typing import List, Dict, Any


class PipelineRequest(BaseModel):
    project_name: str
    sources: List[Dict[str, Any]]
    actions: List[str] = []
    params: Dict[str, Any] = {}
