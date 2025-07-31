"""
BM25 full-text search provider for Aurora-Core Knowledge Base v2.0.

This module provides BM25-based full-text search capabilities,
complementing vector search for hybrid search functionality.
"""

import logging
import math
import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Set

from .interfaces import Document, SearchMethod, SearchResult, FullTextSearchProvider

logger = logging.getLogger(__name__)


class BM25FullTextSearchProvider(FullTextSearchProvider):
    """BM25-based full-text search provider."""
    
    def __init__(self, k1: float = 1.2, b: float = 0.75):
        """
        Initialize BM25 search provider.
        
        Args:
            k1: Term frequency saturation parameter (default: 1.2)
            b: Length normalization parameter (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        
        # Document storage
        self._documents: Dict[str, Document] = {}
        self._doc_lengths: Dict[str, int] = {}
        self._avg_doc_length: float = 0.0
        
        # Inverted index: term -> {doc_id: term_frequency}
        self._inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        
        # Document frequency: term -> number of documents containing term
        self._doc_frequencies: Dict[str, int] = defaultdict(int)
        
        logger.info("BM25 full-text search provider initialized")
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into terms.
        
        Simple tokenization: lowercase, split on non-alphanumeric, remove empty.
        """
        # Convert to lowercase and split on non-alphanumeric characters
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [token for token in tokens if len(token) > 1]  # Remove single character tokens
    
    def _compute_idf(self, term: str) -> float:
        """Compute Inverse Document Frequency for a term."""
        total_docs = len(self._documents)
        if total_docs == 0:
            return 0.0
        
        doc_freq = self._doc_frequencies[term]
        if doc_freq == 0:
            return 0.0
        
        # IDF = log((N - df + 0.5) / (df + 0.5))
        idf = math.log((total_docs - doc_freq + 0.5) / (doc_freq + 0.5))
        return max(0.0, idf)  # Ensure non-negative
    
    def _compute_bm25_score(self, query_terms: List[str], doc_id: str) -> float:
        """Compute BM25 score for a document given query terms."""
        if doc_id not in self._documents:
            return 0.0
        
        doc_length = self._doc_lengths[doc_id]
        score = 0.0
        
        # Count query term frequencies
        query_term_freqs = Counter(query_terms)
        
        for term, query_freq in query_term_freqs.items():
            if term not in self._inverted_index or doc_id not in self._inverted_index[term]:
                continue
            
            # Term frequency in document
            tf = self._inverted_index[term][doc_id]
            
            # IDF
            idf = self._compute_idf(term)
            
            # BM25 formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self._avg_doc_length))
            
            term_score = idf * (numerator / denominator)
            score += term_score
        
        return score
    
    def _update_statistics(self) -> None:
        """Update average document length and other statistics."""
        if not self._documents:
            self._avg_doc_length = 0.0
            return
        
        total_length = sum(self._doc_lengths.values())
        self._avg_doc_length = total_length / len(self._documents)
    
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the BM25 index."""
        if not documents:
            return
        
        for doc in documents:
            # Store document
            self._documents[doc.id] = doc
            
            # Tokenize content
            tokens = self._tokenize(doc.content)
            self._doc_lengths[doc.id] = len(tokens)
            
            # Update inverted index
            term_freqs = Counter(tokens)
            
            for term, freq in term_freqs.items():
                # Update inverted index
                self._inverted_index[term][doc.id] = freq
                
                # Update document frequency if this is the first occurrence in this doc
                if freq > 0 and doc.id not in self._inverted_index[term]:
                    self._doc_frequencies[term] += 1
        
        # Update statistics
        self._update_statistics()
        
        logger.info(f"Added {len(documents)} documents to BM25 index. Total: {len(self._documents)}")
    
    async def search(self, query: str, limit: int = 10,
                    filters: Optional[Dict[str, Any]] = None) -> List[SearchResult]:
        """Perform BM25 full-text search."""
        if not self._documents:
            return []
        
        # Tokenize query
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        
        # Score all documents
        doc_scores = []
        
        for doc_id in self._documents:
            # Apply filters if provided
            if filters:
                doc = self._documents[doc_id]
                doc_metadata = doc.metadata or {}
                
                # Simple filter matching
                filter_match = True
                for filter_key, filter_value in filters.items():
                    if filter_key not in doc_metadata or doc_metadata[filter_key] != filter_value:
                        filter_match = False
                        break
                
                if not filter_match:
                    continue
            
            score = self._compute_bm25_score(query_terms, doc_id)
            if score > 0:
                doc_scores.append((doc_id, score))
        
        # Sort by score descending
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Convert to SearchResult objects
        results = []
        for doc_id, score in doc_scores[:limit]:
            doc = self._documents[doc_id]
            results.append(SearchResult(
                document_id=doc_id,
                content=doc.content,
                score=score,
                metadata=doc.metadata,
                search_method=SearchMethod.BM25
            ))
        
        logger.debug(f"BM25 search for '{query}' returned {len(results)} results")
        return results
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document from the BM25 index."""
        if document_id not in self._documents:
            return False
        
        try:
            # Remove from documents
            doc = self._documents.pop(document_id)
            self._doc_lengths.pop(document_id, None)
            
            # Update inverted index and document frequencies
            tokens = self._tokenize(doc.content)
            term_freqs = Counter(tokens)
            
            for term in term_freqs:
                if term in self._inverted_index and document_id in self._inverted_index[term]:
                    # Remove document from inverted index
                    del self._inverted_index[term][document_id]
                    
                    # Update document frequency
                    self._doc_frequencies[term] -= 1
                    if self._doc_frequencies[term] <= 0:
                        del self._doc_frequencies[term]
                    
                    # Clean up empty term entries
                    if not self._inverted_index[term]:
                        del self._inverted_index[term]
            
            # Update statistics
            self._update_statistics()
            
            logger.info(f"Deleted document {document_id} from BM25 index")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document {document_id} from BM25 index: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the BM25 index."""
        return {
            "total_documents": len(self._documents),
            "total_terms": len(self._inverted_index),
            "average_document_length": self._avg_doc_length,
            "parameters": {
                "k1": self.k1,
                "b": self.b
            }
        }
    
    def search_terms(self, terms: List[str]) -> Dict[str, List[str]]:
        """Get documents containing specific terms (for debugging)."""
        term_docs = {}
        for term in terms:
            term_lower = term.lower()
            if term_lower in self._inverted_index:
                term_docs[term] = list(self._inverted_index[term_lower].keys())
            else:
                term_docs[term] = []
        return term_docs