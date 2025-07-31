from typing import Optional
import chromadb
import os
from typing import List, Dict, Any
from chromadb.api.models.Collection import Collection
import logging
from aurora_platform.config import settings


class KnowledgeBaseService:
    # Métodos mínimos já definidos acima
    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: Dict[str, Any],
        collection_name: str = "default_knowledge_base",
    ) -> None:
        """
        Adiciona um único documento à coleção especificada.
        Compatível com chamadas antigas.
        """
        self.add_documents(
            [
                {
                    "document_id": document_id,
                    "text": text,
                    "metadata": metadata,
                }
            ],
            collection_name=collection_name,
        )

    def ingest_document(
        self,
        document_id: str,
        text: str,
        metadata: Dict[str, Any],
        collection_name: str = "default_knowledge_base",
    ) -> None:
        """
        Método compatível com interface nova, equivalente ao add_document.
        """
        self.add_document(document_id, text, metadata, collection_name)

    def retrieve(
        self,
        query: str,
        collection_name: str = "default_knowledge_base",
        n_results: int = 5,
    ) -> List[Dict]:
        """
        Compatível com interface antiga, delega para query_collection.
        """
        return self.query_collection(query, collection_name, n_results)

    def __init__(self, persist_directory: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_DB_PATH", "chroma_data"
        )
        self.client = None
        self.collections = {}
        self._initialize_client()
        self._ensure_collection("default_knowledge_base")

    def _ensure_collection(self, collection_name: str):
        if self.client is None:
            self._initialize_client()
        try:
            if self.client is not None:
                # ChromaDB >=0.4.22 usa get_or_create_collection, versões antigas usam get_collection/create_collection
                if hasattr(self.client, "get_or_create_collection"):
                    self.collections[collection_name] = (
                        self.client.get_or_create_collection(collection_name)
                    )
                else:
                    try:
                        self.collections[collection_name] = self.client.get_collection(
                            collection_name
                        )
                    except Exception:
                        self.collections[collection_name] = (
                            self.client.create_collection(collection_name)
                        )
        except Exception as e:
            self.logger.error(f"Erro ao acessar coleção: {e}")

    def _initialize_client(self) -> None:
        """Inicializa o cliente ChromaDB apenas se necessário"""
        if self.client is None:
            try:
                self.client = chromadb.PersistentClient(path=self.persist_directory)
                self.logger.info(
                    f"ChromaDB client initialized at {self.persist_directory}"
                )
            except Exception as e:
                self.logger.error(f"ChromaDB initialization failed: {str(e)}")
                raise RuntimeError("Failed to initialize ChromaDB client") from e

    def add_documents(
        self, documents: List[Dict[str, Any]], collection_name: str
    ) -> int:
        collection = self.collections.get(collection_name)
        if collection is None:
            self._ensure_collection(collection_name)
            collection = self.collections.get(collection_name)
        if collection is None:
            self.logger.error(
                f"Coleção '{collection_name}' não encontrada ou não pôde ser criada."
            )
            return 0
        try:
            for doc in documents:
                if hasattr(collection, "add"):
                    collection.add(
                        ids=[doc.get("document_id")],
                        documents=[doc.get("text")],
                        metadatas=[doc.get("metadata")],
                    )
                    self.logger.info(
                        f"Document {doc.get('document_id')} added successfully to collection {collection_name}"
                    )
            return len(documents)
        except Exception as e:
            self.logger.error(f"Erro ao adicionar documentos: {e}")
            return 0

    def query_collection(
        self, query: str, collection_name: str, n_results: int = 5
    ) -> List[Dict]:
        collection = self.collections.get(collection_name)
        if collection is None:
            self._ensure_collection(collection_name)
            collection = self.collections.get(collection_name)
        if collection is None:
            self.logger.error(
                f"Coleção '{collection_name}' não encontrada ou não pôde ser criada."
            )
            return []
        try:
            if hasattr(collection, "query"):
                results = collection.query(query_texts=[query], n_results=n_results)
                return results
            else:
                self.logger.error(
                    f"Método 'query' não disponível na coleção '{collection_name}'."
                )
                return []
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve documents for query '{query}' in collection '{collection_name}': {e}"
            )
            return []

    def get_collection(self, collection_name: str) -> Collection | None:
        return self.collections.get(collection_name)

    def delete_collection(self, collection_name: str):
        collection = self.collections.get(collection_name)
        if collection and hasattr(collection, "delete"):
            collection.delete()
