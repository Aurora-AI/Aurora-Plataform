from sentence_transformers import SentenceTransformer
from typing import List
import re
import logging

logger = logging.getLogger(__name__)


class SemanticAnalysisService:
    def __init__(self):
        try:
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Modelo de embeddings carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            self.embedder = None

    def is_document_coherent(self, text_sample: str) -> bool:
        """Verifica se o documento tem conteúdo útil"""
        if not text_sample or len(text_sample.strip()) < 50:
            return False

        # Verifica se não é apenas boilerplate
        boilerplate_patterns = [
            r"^\s*page \d+",
            r"^\s*\d+\s*$",
            r"^\s*copyright",
            r"^\s*all rights reserved",
        ]

        clean_text = text_sample.lower().strip()
        for pattern in boilerplate_patterns:
            if re.match(pattern, clean_text):
                return False

        # Verifica densidade de palavras úteis
        words = clean_text.split()
        if len(words) < 10:
            return False

        return True

    def semantic_chunking(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Fragmentação semântica melhorada"""
        if not text.strip():
            return []

        # Divide por parágrafos primeiro
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [text]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Se o parágrafo sozinho é maior que o limite, divide por sentenças
            if len(paragraph) > max_chunk_size:
                sentences = re.split(r"[.!?]+", paragraph)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue

                    if len(current_chunk) + len(sentence) > max_chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        current_chunk += (" " if current_chunk else "") + sentence
            else:
                # Adiciona parágrafo inteiro se couber
                if len(current_chunk) + len(paragraph) > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    current_chunk += ("\n\n" if current_chunk else "") + paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        return [chunk for chunk in chunks if len(chunk.strip()) > 20]
