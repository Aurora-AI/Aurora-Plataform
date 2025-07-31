from pydantic import BaseModel
from typing import List


class KnowledgeQuery(BaseModel):
    query: str
    n_results: int = 5
    collection_name: str = "default_knowledge_base"


class SearchResult(BaseModel):
    results: List[str]


class IngestionRequest(BaseModel):
    source_type: str  # Ex: "url", "file_upload"
    source_path: str  # A URL ou o identificador do arquivo
    collection_name: str = "default_knowledge_base"


class IngestURLRequest(BaseModel):
    url: str
    collection_name: str = "default_knowledge_base"
