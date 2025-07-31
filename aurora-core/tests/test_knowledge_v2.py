"""
Test suite for Aurora-Core Knowledge Base Service v2.0.
"""

import pytest

from src.aurora_platform.services.knowledge_v2 import (
    BM25FullTextSearchProvider,
    Document,
    HybridKnowledgeBaseService,
    KnowledgeServiceV2,
    RerankingMethod,
    SearchMethod,
    SearchQuery,
)


class TestDocument:
    """Test cases for Document data model."""
    
    def test_document_creation(self):
        """Test document creation."""
        doc = Document(
            id="test_doc",
            content="This is test content",
            metadata={"type": "test"}
        )
        
        assert doc.id == "test_doc"
        assert doc.content == "This is test content"
        assert doc.metadata["type"] == "test"
        assert doc.embeddings is None


class TestBM25FullTextSearchProvider:
    """Test cases for BM25 search provider."""
    
    @pytest.fixture
    def bm25_provider(self):
        """Create BM25 provider for testing."""
        return BM25FullTextSearchProvider()
    
    @pytest.fixture
    def sample_documents(self):
        """Create sample documents for testing."""
        return [
            Document(
                id="doc1",
                content="Python programming language tutorial for beginners",
                metadata={"category": "tutorial", "language": "python"}
            ),
            Document(
                id="doc2", 
                content="Machine learning algorithms and artificial intelligence",
                metadata={"category": "ai", "topic": "ml"}
            ),
            Document(
                id="doc3",
                content="Database design patterns and best practices",
                metadata={"category": "database", "topic": "design"}
            )
        ]
    
    async def test_add_documents(self, bm25_provider, sample_documents):
        """Test adding documents to BM25 index."""
        await bm25_provider.add_documents(sample_documents)
        
        stats = bm25_provider.get_index_stats()
        assert stats["total_documents"] == 3
        assert stats["total_terms"] > 0
        assert stats["average_document_length"] > 0
    
    async def test_search_exact_match(self, bm25_provider, sample_documents):
        """Test BM25 search with exact term matches."""
        await bm25_provider.add_documents(sample_documents)
        
        results = await bm25_provider.search("python programming", limit=5)
        
        assert len(results) > 0
        assert results[0].document_id == "doc1"  # Should find Python doc
        assert results[0].score > 0
    
    async def test_search_partial_match(self, bm25_provider, sample_documents):
        """Test BM25 search with partial matches."""
        await bm25_provider.add_documents(sample_documents)
        
        results = await bm25_provider.search("learning", limit=5)
        
        assert len(results) > 0
        # Should find machine learning doc
        assert any(r.document_id == "doc2" for r in results)
    
    async def test_search_no_match(self, bm25_provider, sample_documents):
        """Test BM25 search with no matches."""
        await bm25_provider.add_documents(sample_documents)
        
        results = await bm25_provider.search("nonexistent terms xyz", limit=5)
        
        assert len(results) == 0
    
    async def test_delete_document(self, bm25_provider, sample_documents):
        """Test document deletion."""
        await bm25_provider.add_documents(sample_documents)
        
        # Delete one document
        success = await bm25_provider.delete_document("doc1")
        assert success
        
        # Verify it's gone
        stats = bm25_provider.get_index_stats()
        assert stats["total_documents"] == 2
        
        # Search should not find it
        results = await bm25_provider.search("python programming", limit=5)
        assert all(r.document_id != "doc1" for r in results)


class TestSearchQuery:
    """Test cases for SearchQuery model."""
    
    def test_default_query(self):
        """Test default search query."""
        query = SearchQuery(query="test query")
        
        assert query.query == "test query"
        assert query.method == SearchMethod.HYBRID
        assert query.limit == 10
        assert query.rerank == RerankingMethod.CROSS_ENCODER
        assert query.filters is None
    
    def test_custom_query(self):
        """Test custom search query."""
        query = SearchQuery(
            query="custom query",
            method=SearchMethod.VECTOR,
            limit=5,
            rerank=RerankingMethod.NONE,
            filters={"category": "test"}
        )
        
        assert query.method == SearchMethod.VECTOR
        assert query.limit == 5
        assert query.rerank == RerankingMethod.NONE
        assert query.filters["category"] == "test"


class TestKnowledgeServiceV2:
    """Test cases for Knowledge Service v2 facade."""
    
    @pytest.fixture
    def knowledge_service(self):
        """Create knowledge service for testing."""
        # Note: This will try to connect to ChromaDB, but should gracefully degrade
        return KnowledgeServiceV2()
    
    async def test_add_single_document(self, knowledge_service):
        """Test adding a single document."""
        # This tests the compatibility method
        await knowledge_service.add_document(
            document_id="test_doc",
            text="Test document content",
            metadata={"type": "test"}
        )
        # If no error is raised, the test passes
        assert True
    
    async def test_retrieve_documents(self, knowledge_service):
        """Test retrieving documents."""
        # Add a document first
        await knowledge_service.add_document(
            document_id="search_test",
            text="This is searchable content about Python programming",
            metadata={"type": "tutorial"}
        )
        
        # Search for it (will use BM25 since ChromaDB might not be available)
        results = await knowledge_service.retrieve("python programming", top_k=5)
        
        # Should return list format for compatibility
        assert isinstance(results, list)
        
        # If we found results, verify format
        if results:
            result = results[0]
            assert "text" in result
            assert "score" in result
            assert "metadata" in result
            assert "document_id" in result
    
    async def test_get_stats(self, knowledge_service):
        """Test getting service statistics."""
        stats = await knowledge_service.get_service_stats()
        
        assert "service_version" in stats
        assert stats["service_version"] == "2.0"
        assert "vector_search" in stats
        assert "bm25_search" in stats
        assert "reranking" in stats


class TestHybridKnowledgeBaseService:
    """Test cases for the main hybrid service."""
    
    @pytest.fixture
    def hybrid_service(self):
        """Create hybrid service for testing."""
        return HybridKnowledgeBaseService()
    
    @pytest.fixture
    def test_documents(self):
        """Create test documents."""
        return [
            Document(
                id="hybrid_doc1",
                content="Advanced Python programming techniques and patterns",
                metadata={"category": "programming", "level": "advanced"}
            ),
            Document(
                id="hybrid_doc2",
                content="Introduction to machine learning with Python",
                metadata={"category": "ai", "level": "beginner"}
            )
        ]
    
    async def test_add_documents(self, hybrid_service, test_documents):
        """Test adding documents to hybrid service."""
        await hybrid_service.add_documents(test_documents)
        # If no error is raised, the test passes
        assert True
    
    async def test_bm25_search(self, hybrid_service, test_documents):
        """Test BM25-only search."""
        await hybrid_service.add_documents(test_documents)
        
        query = SearchQuery(
            query="python programming",
            method=SearchMethod.BM25,
            limit=5,
            rerank=RerankingMethod.NONE
        )
        
        response = await hybrid_service.search(query)
        
        assert response.query == "python programming"
        assert response.search_method == SearchMethod.BM25
        assert response.processing_time_ms > 0
        assert isinstance(response.results, list)
    
    async def test_hybrid_search(self, hybrid_service, test_documents):
        """Test hybrid search."""
        await hybrid_service.add_documents(test_documents)
        
        query = SearchQuery(
            query="machine learning python",
            method=SearchMethod.HYBRID,
            limit=5,
            rerank=RerankingMethod.SIMILARITY_WEIGHTED
        )
        
        response = await hybrid_service.search(query)
        
        assert response.search_method == SearchMethod.HYBRID
        assert response.reranking_applied
        assert isinstance(response.results, list)
    
    async def test_service_health(self, hybrid_service):
        """Test service health check."""
        # BM25 should always be available, vector might not be
        is_healthy = hybrid_service.is_healthy()
        assert isinstance(is_healthy, bool)
    
    async def test_get_comprehensive_stats(self, hybrid_service):
        """Test getting comprehensive service statistics."""
        stats = await hybrid_service.get_stats()
        
        assert "service_version" in stats
        assert "vector_search" in stats
        assert "bm25_search" in stats
        assert "reranking" in stats
        assert "hybrid_weights" in stats
        
        # Check BM25 is available
        assert stats["bm25_search"]["available"] is True