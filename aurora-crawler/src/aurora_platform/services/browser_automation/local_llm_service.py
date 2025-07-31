import logging
from transformers.pipelines import pipeline

logger = logging.getLogger(__name__)


class LocalLLMService:
    """
    Serviço para sumarização de texto usando modelo local via HuggingFace Transformers.
    """

    def __init__(self, model_name: str = "philschmid/tiny-llama-summarization"):
        self.model_name = model_name
        self._summarizer = None

    def _load_pipeline(self):
        if self._summarizer is None:
            logger.info(f"Carregando modelo de sumarização: {self.model_name}")
            try:
                self._summarizer = pipeline("summarization", model=self.model_name)
            except Exception as e:
                logger.error(f"Erro ao carregar pipeline: {e}")
                raise RuntimeError("Falha ao carregar pipeline de sumarização.")

    def summarize(self, text: str, max_length: int = 128, min_length: int = 32) -> str:
        self._load_pipeline()
        if self._summarizer is None:
            raise RuntimeError("Pipeline de sumarização não carregado.")
        result = self._summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return result[0]["summary_text"]
