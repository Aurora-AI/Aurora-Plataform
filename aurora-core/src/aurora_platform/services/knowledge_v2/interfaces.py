"""
Interfaces and data models for Knowledge Base Service v2.0.

This module defines the core interfaces for hybrid search functionality,
including vector search, full-text search, and re-ranking.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class SearchMethod(Enum):
    """Available search methods."""
    VECTOR = "vector"
    BM25 = "bm25"
    HYBRID = "hybrid"


class RerankingMethod(Enum):
    """Available re-ranking methods."""
    NONE = "none"
    CROSS_ENCODER = "cross_encoder"
    SIMILARITY_WEIGHTED = "similarity_weighted"


@dataclass
class SearchResult:
    """Individual search result."""
    document_id: str
    content: str
    score: float
    metadata: Optional[Dict[str, Any]] = None
    search_method: Optional[SearchMethod] = None


@dataclass
class SearchQuery:
    """Search query with configuration."""
    query: str
    method: SearchMethod = SearchMethod.HYBRID
    limit: int = 10
    rerank: RerankingMethod = RerankingMethod.CROSS_ENCODER
    filters: Optional[Dict[str, Any]] = None


@dataclass
class SearchResponse:
    """Complete search response."""
    query: str
    results: List[SearchResult]
    total_found: int
    search_method: SearchMethod
    reranking_applied: bool
    processing_time_ms: float
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Document:
    """Document for ingestion."""
    id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    embeddings: Optional[List[float]] = None


class VectorSearchProvider(ABC):
    """Interface for vector search providers."""
    
    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10, 
                    filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Perform vector search."""
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID."""
        pass


class FullTextSearchProvider(ABC):
    """Interface for full-text search providers."""
    
    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the full-text index."""
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10,
                    filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Perform full-text search."""
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID."""
        pass


class RerankingProvider(ABC):
    """Interface for result re-ranking providers."""
    
    @abstractmethod
    async def rerank(self, query: str, results: List[SearchResult], 
                    limit: Optional[int] = None) -> List[SearchResult]:
        """Re-rank search results."""
        pass


class KnowledgeBaseProvider(ABC):
    """Main interface for knowledge base operations."""
    
    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the knowledge base."""
        pass
    
    @abstractmethod
    async def search(self, search_query: SearchQuery) -> SearchResponse:
        """Perform hybrid search."""
        pass
    
    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document."""
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        pass