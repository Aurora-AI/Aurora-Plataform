# Aurora-Core Knowledge Base Service v2.0
#
# Enhanced knowledge base service with hybrid search capabilities:
# - Vector search using ChromaDB
# - BM25 full-text search
# - Cross-Encoder re-ranking
# - Modular architecture for advanced AI modules

from .bm25_search import BM25FullTextSearchProvider
from .hybrid_service import HybridKnowledgeBaseService, KnowledgeServiceV2, create_hybrid_knowledge_service
from .interfaces import (
    Document,
    KnowledgeBaseProvider,
    RerankingMethod,
    SearchMethod,
    SearchQuery,
    SearchResponse,
    SearchResult,
)
from .reranking import CrossEncoderRerankingProvider, SimilarityWeightedRerankingProvider
from .vector_search import ChromaVectorSearchProvider

__all__ = [
    # Main service classes
    "HybridKnowledgeBaseService",
    "KnowledgeServiceV2",
    
    # Search providers
    "ChromaVectorSearchProvider", 
    "BM25FullTextSearchProvider",
    
    # Re-ranking providers
    "CrossEncoderRerankingProvider",
    "SimilarityWeightedRerankingProvider",
    
    # Data models and interfaces
    "Document",
    "SearchQuery",
    "SearchResponse", 
    "SearchResult",
    "SearchMethod",
    "RerankingMethod",
    "KnowledgeBaseProvider",
    
    # Convenience functions
    "create_hybrid_knowledge_service",
]