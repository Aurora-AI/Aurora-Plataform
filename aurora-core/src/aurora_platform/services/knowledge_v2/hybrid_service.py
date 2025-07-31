"""
Hybrid Knowledge Base Service v2.0 for Aurora-Core.

This service combines vector search, BM25 full-text search, and re-ranking
to provide advanced hybrid search capabilities for the Aurora platform.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from .bm25_search import BM25FullTextSearchProvider
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

logger = logging.getLogger(__name__)


class HybridKnowledgeBaseService(KnowledgeBaseProvider):
    """
    Hybrid Knowledge Base Service that combines multiple search methods.
    
    This service provides:
    - Vector search using ChromaDB
    - BM25 full-text search
    - Cross-Encoder re-ranking
    - Configurable hybrid search strategies
    """
    
    def __init__(self, 
                 vector_host: str = "chromadb", 
                 vector_port: int = 8000,
                 collection_name: str = "aurora_knowledge_v2"):
        """
        Initialize the hybrid knowledge base service.
        
        Args:
            vector_host: ChromaDB host
            vector_port: ChromaDB port
            collection_name: ChromaDB collection name
        """
        # Initialize search providers
        self.vector_provider = ChromaVectorSearchProvider(
            host=vector_host,
            port=vector_port,
            collection_name=collection_name
        )
        
        self.bm25_provider = BM25FullTextSearchProvider()
        
        # Initialize re-ranking providers
        self.cross_encoder_reranker = CrossEncoderRerankingProvider()
        self.similarity_reranker = SimilarityWeightedRerankingProvider()
        
        # Configuration
        self.default_hybrid_weights = {
            "vector": 0.6,
            "bm25": 0.4
        }
        
        logger.info("Hybrid Knowledge Base Service v2.0 initialized")
    
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to both vector and BM25 indexes."""
        if not documents:
            logger.warning("No documents provided for addition")
            return
        
        # Add to vector store
        try:
            await self.vector_provider.add_documents(documents)
            logger.debug(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
        
        # Add to BM25 index
        try:
            await self.bm25_provider.add_documents(documents)
            logger.debug(f"Added {len(documents)} documents to BM25 index")
        except Exception as e:
            logger.error(f"Failed to add documents to BM25 index: {e}")
        
        logger.info(f"Successfully added {len(documents)} documents to hybrid knowledge base")
    
    async def search(self, search_query: SearchQuery) -> SearchResponse:
        """Perform hybrid search with optional re-ranking."""
        start_time = time.time()
        
        try:
            if search_query.method == SearchMethod.VECTOR:
                results = await self._vector_search(search_query)
            elif search_query.method == SearchMethod.BM25:
                results = await self._bm25_search(search_query)
            elif search_query.method == SearchMethod.HYBRID:
                results = await self._hybrid_search(search_query)
            else:
                raise ValueError(f"Unsupported search method: {search_query.method}")
            
            # Apply re-ranking if requested
            reranking_applied = False
            if search_query.rerank != RerankingMethod.NONE and results:
                results = await self._apply_reranking(search_query, results)
                reranking_applied = True
            
            # Limit results
            if len(results) > search_query.limit:
                results = results[:search_query.limit]
            
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            response = SearchResponse(
                query=search_query.query,
                results=results,
                total_found=len(results),
                search_method=search_query.method,
                reranking_applied=reranking_applied,
                processing_time_ms=processing_time,
                metadata={
                    "filters_applied": search_query.filters is not None,
                    "reranking_method": search_query.rerank.value if reranking_applied else None
                }
            )
            
            logger.debug(f"Search completed in {processing_time:.2f}ms, found {len(results)} results")
            return response
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            processing_time = (time.time() - start_time) * 1000
            
            return SearchResponse(
                query=search_query.query,
                results=[],
                total_found=0,
                search_method=search_query.method,
                reranking_applied=False,
                processing_time_ms=processing_time,
                metadata={"error": str(e)}
            )
    
    async def _vector_search(self, search_query: SearchQuery) -> List[SearchResult]:
        """Perform vector search only."""
        return await self.vector_provider.search(
            query=search_query.query,
            limit=search_query.limit * 2,  # Get more results for potential re-ranking
            filters=search_query.filters
        )
    
    async def _bm25_search(self, search_query: SearchQuery) -> List[SearchResult]:
        """Perform BM25 search only."""
        return await self.bm25_provider.search(
            query=search_query.query,
            limit=search_query.limit * 2,  # Get more results for potential re-ranking
            filters=search_query.filters
        )
    
    async def _hybrid_search(self, search_query: SearchQuery) -> List[SearchResult]:
        """Perform hybrid search combining vector and BM25."""
        # Run both searches concurrently
        vector_results = await self._vector_search(search_query)
        bm25_results = await self._bm25_search(search_query)
        
        # Combine results by document ID
        combined_results = {}
        
        # Add vector results
        for result in vector_results:
            combined_results[result.document_id] = result
        
        # Add BM25 results (merge if document already exists)
        for result in bm25_results:
            if result.document_id in combined_results:
                # Document found in both searches - we'll handle this in re-ranking
                existing = combined_results[result.document_id]
                # Keep the original but add BM25 score to metadata
                if existing.metadata is None:
                    existing.metadata = {}
                existing.metadata["bm25_score"] = result.score
            else:
                # Document only found in BM25
                combined_results[result.document_id] = result
        
        # Convert back to list and sort by original scores
        all_results = list(combined_results.values())
        all_results.sort(key=lambda x: x.score, reverse=True)
        
        logger.debug(f"Hybrid search: vector={len(vector_results)}, bm25={len(bm25_results)}, combined={len(all_results)}")
        return all_results
    
    async def _apply_reranking(self, search_query: SearchQuery, 
                              results: List[SearchResult]) -> List[SearchResult]:
        """Apply re-ranking to search results."""
        if search_query.rerank == RerankingMethod.CROSS_ENCODER:
            return await self.cross_encoder_reranker.rerank(
                query=search_query.query,
                results=results,
                limit=search_query.limit
            )
        elif search_query.rerank == RerankingMethod.SIMILARITY_WEIGHTED:
            return await self.similarity_reranker.rerank(
                query=search_query.query,
                results=results,
                limit=search_query.limit
            )
        else:
            return results
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document from both indexes."""
        vector_success = await self.vector_provider.delete_document(document_id)
        bm25_success = await self.bm25_provider.delete_document(document_id)
        
        success = vector_success or bm25_success
        if success:
            logger.info(f"Document {document_id} deleted from knowledge base")
        else:
            logger.warning(f"Failed to delete document {document_id}")
        
        return success
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the knowledge base."""
        vector_stats = {}
        if self.vector_provider.is_available():
            vector_stats = await self.vector_provider.get_collection_stats()
        
        bm25_stats = self.bm25_provider.get_index_stats()
        
        return {
            "service_version": "2.0",
            "vector_search": {
                "provider": "ChromaDB",
                "available": self.vector_provider.is_available(),
                **vector_stats
            },
            "bm25_search": {
                "provider": "BM25",
                "available": True,
                **bm25_stats
            },
            "reranking": {
                "cross_encoder": {
                    "available": self.cross_encoder_reranker.is_available(),
                    **self.cross_encoder_reranker.get_model_info()
                },
                "similarity_weighted": {
                    "available": True,
                    "vector_weight": self.similarity_reranker.vector_weight,
                    "bm25_weight": self.similarity_reranker.bm25_weight
                }
            },
            "hybrid_weights": self.default_hybrid_weights
        }
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy and ready to serve requests."""
        return self.vector_provider.is_available() or True  # BM25 is always available


# Convenience functions for backward compatibility
async def create_hybrid_knowledge_service(**kwargs) -> HybridKnowledgeBaseService:
    """Create and return a hybrid knowledge base service instance."""
    return HybridKnowledgeBaseService(**kwargs)


class KnowledgeServiceV2:
    """
    Facade class for easy integration with existing Aurora-Core code.
    
    This class provides a simple interface that can gradually replace
    the existing knowledge service while maintaining compatibility.
    """
    
    def __init__(self, **kwargs):
        self._service = HybridKnowledgeBaseService(**kwargs)
    
    async def add_document(self, document_id: str, text: str, 
                          metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a single document (compatibility method)."""
        doc = Document(id=document_id, content=text, metadata=metadata)
        await self._service.add_documents([doc])
    
    async def retrieve(self, query: str, top_k: int = 10, 
                      method: str = "hybrid") -> List[Dict[str, Any]]:
        """Retrieve documents (compatibility method)."""
        search_method = SearchMethod.HYBRID
        if method == "vector":
            search_method = SearchMethod.VECTOR
        elif method == "bm25":
            search_method = SearchMethod.BM25
        
        search_query = SearchQuery(
            query=query,
            method=search_method,
            limit=top_k,
            rerank=RerankingMethod.CROSS_ENCODER
        )
        
        response = await self._service.search(search_query)
        
        # Convert to legacy format
        return [
            {
                "text": result.content,
                "score": result.score,
                "metadata": result.metadata or {},
                "document_id": result.document_id
            }
            for result in response.results
        ]
    
    async def get_service_stats(self) -> Dict[str, Any]:
        """Get service statistics."""
        return await self._service.get_stats()