import fitz
import docx
import os
import logging
from typing import Dict, Any
from typing import Sequence, List, Dict, Any
from .knowledge_service import KnowledgeBaseService

logger = logging.getLogger(__name__)


class DocumentProcessingService:
    def extract_text_from_excel(self, filepath: str) -> Sequence[Dict[Any, Any]]:
        """
        Extrai o conteúdo de um arquivo Excel (.xls/.xlsx) e retorna uma lista de dicionários.
        Cada item da lista representa uma linha do Excel.
        """
        import pandas as pd

        try:
            df = pd.read_excel(filepath, engine=None)
            data = df.replace({pd.NA: None}).to_dict(orient="records")
            return data  # Retorna lista concreta
        except Exception as e:
            logger.error(f"Erro ao processar Excel: {e}")
            raise ValueError(f"Falha no processamento do Excel: {str(e)}") from e

    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service

    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extrai o texto de um PDF usando PyMuPDF (fitz)."""
        try:
            doc = fitz.open(filepath)
            text = "\n".join(
                page.get_text() if hasattr(page, "get_text") else str(page)  # type: ignore
                for page in doc
            )
            doc.close()
            return text
        except Exception as e:
            logger.error(f"Erro ao processar PDF: {e}")
            return ""

    def extract_text_from_docx(self, filepath: str) -> str:
        """Extrai o texto de um arquivo DOCX."""
        try:
            document = docx.Document(filepath)
            return "\n".join([para.text for para in document.paragraphs])
        except Exception as e:
            logger.error(f"Erro ao processar DOCX: {str(e)}")
            return ""

    def process_and_ingest_files(
        self, file_paths: List[str], collection_name: str
    ) -> List[str]:
        """Processa uma lista de arquivos de diferentes formatos e os ingere na base de conhecimento."""
        ingested_ids = []
        for path in file_paths:
            filename = os.path.basename(path)
            text = ""
            try:
                if filename.lower().endswith(".pdf"):
                    text = self.extract_text_from_pdf(path)
                elif filename.lower().endswith((".docx", ".doc")):
                    text = self.extract_text_from_docx(path)
                elif filename.lower().endswith((".xls", ".xlsx")):
                    excel_data = self.extract_text_from_excel(path)
                    text = str(excel_data)
                else:
                    logger.warning(
                        f"Formato de arquivo não suportado, ignorando: {filename}"
                    )
                if text.strip():
                    doc_id = f"file_{filename}"
                    metadata = {"source": f"local_upload_{filename}"}
                    self.kb_service.add_document(
                        document_id=doc_id,
                        text=text,
                        metadata=metadata,
                        collection_name=collection_name,
                    )
                    ingested_ids.append(doc_id)
                else:
                    logger.warning(f"Nenhum texto extraído do arquivo: {path}")
            except Exception as e:
                logger.error(f"Falha ao processar o arquivo {path}: {e}")
        return ingested_ids

    def process_and_ingest_sources(
        self, sources: List[Dict[str, Any]], collection_name: str
    ) -> List[str]:
        """Processa múltiplas fontes (URLs e arquivos)."""
        ingested_ids = []
        for source in sources:
            try:
                if source.get("source_type") == "file":
                    ingested_ids.extend(
                        self.process_and_ingest_files(
                            [source["source_path"]], collection_name=collection_name
                        )
                    )
                # Se for URL, lógica de scraping entraria aqui
            except Exception as e:
                logger.error(f"Erro ao processar fonte {source}: {e}")
        return ingested_ids


if __name__ == "__main__":
    os.environ["PYTHONPATH"] = "src"
    from aurora_platform.main import app
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
