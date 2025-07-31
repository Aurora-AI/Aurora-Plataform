"""
ChromaDB vector search provider for Aurora-Core Knowledge Base v2.0.

This module provides vector search capabilities using ChromaDB,
integrating with the existing ChromaDB infrastructure.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings

from .interfaces import Document, SearchMethod, SearchResult, VectorSearchProvider

logger = logging.getLogger(__name__)


class ChromaVectorSearchProvider(VectorSearchProvider):
    """Vector search provider using ChromaDB."""
    
    def __init__(self, host: str = "chromadb", port: int = 8000, 
                 collection_name: str = "aurora_knowledge_v2"):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self._client: Optional[ClientAPI] = None
        self._collection = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize ChromaDB client and collection."""
        try:
            self._client = chromadb.HttpClient(
                host=self.host,
                port=self.port,
                settings=Settings(anonymized_telemetry=False),
            )
            
            # Test connection
            self._client.heartbeat()
            
            # Get or create collection
            try:
                self._collection = self._client.get_collection(name=self.collection_name)
                logger.info(f"Connected to existing ChromaDB collection: {self.collection_name}")
            except Exception:
                self._collection = self._client.create_collection(name=self.collection_name)
                logger.info(f"Created new ChromaDB collection: {self.collection_name}")
                
        except Exception as e:
            logger.warning(f"Failed to initialize ChromaDB client: {e}")
            # Set to None to allow graceful degradation
            self._client = None
            self._collection = None
    
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to ChromaDB vector store."""
        if not self._collection:
            raise RuntimeError("ChromaDB not available")
        
        if not documents:
            return
        
        # Prepare data for ChromaDB
        ids = [doc.id for doc in documents]
        texts = [doc.content for doc in documents]
        metadatas = []
        embeddings = []
        
        for doc in documents:
            # Prepare metadata
            metadata = doc.metadata or {}
            metadata.update({
                "content_length": len(doc.content),
                "document_type": "knowledge_v2"
            })
            metadatas.append(metadata)
            
            # Use provided embeddings if available
            if doc.embeddings:
                embeddings.append(doc.embeddings)
        
        try:
            # Add to ChromaDB
            if embeddings:
                self._collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas,
                    embeddings=embeddings
                )
            else:
                # Let ChromaDB generate embeddings
                self._collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas
                )
            
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            
        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {e}")
            raise
    
    async def search(self, query: str, limit: int = 10, 
                    filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Perform vector search using ChromaDB."""
        if not self._collection:
            logger.warning("ChromaDB not available, returning empty results")
            return []
        
        try:
            # Prepare ChromaDB query
            query_params = {
                "query_texts": [query],
                "n_results": limit
            }
            
            # Add filters if provided
            if filters:
                query_params["where"] = filters
            
            # Execute search
            results = self._collection.query(**query_params)
            
            # Convert to SearchResult objects
            search_results = []
            
            if results["documents"] and results["documents"][0]:
                documents = results["documents"][0]
                metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(documents)
                distances = results["distances"][0] if results["distances"] else [0.0] * len(documents)
                ids = results["ids"][0] if results["ids"] else [str(uuid.uuid4()) for _ in documents]
                
                for i, (doc_id, content, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    # Convert distance to similarity score (ChromaDB uses cosine distance)
                    similarity_score = max(0.0, 1.0 - distance)
                    
                    search_results.append(SearchResult(
                        document_id=doc_id,
                        content=content,
                        score=similarity_score,
                        metadata=metadata,
                        search_method=SearchMethod.VECTOR
                    ))
            
            logger.debug(f"Vector search returned {len(search_results)} results")
            return search_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document from ChromaDB."""
        if not self._collection:
            return False
        
        try:
            self._collection.delete(ids=[document_id])
            logger.info(f"Deleted document {document_id} from ChromaDB")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the ChromaDB collection."""
        if not self._collection:
            return {"available": False}
        
        try:
            count = self._collection.count()
            return {
                "available": True,
                "collection_name": self.collection_name,
                "document_count": count,
                "host": self.host,
                "port": self.port
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"available": False, "error": str(e)}
    
    def is_available(self) -> bool:
        """Check if ChromaDB is available."""
        return self._client is not None and self._collection is not None