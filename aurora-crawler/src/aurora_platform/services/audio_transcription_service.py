import os
import tempfile
import logging
import torch
from typing import Optional

logger = logging.getLogger(__name__)


class AudioTranscriptionService:
    def __init__(self, use_gpu: bool = False):
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.model = None
        logger.info(
            f"Inicializando serviço de transcrição no dispositivo: {self.device}"
        )

    def load_model(self):
        """Carrega o modelo Whisper sob demanda"""
        if self.model is None:
            try:
                import whisper  # type: ignore

                logger.info("Carregando modelo Whisper (tiny)...")
                self.model = whisper.load_model("tiny", device=self.device)
            except ImportError:
                logger.error(
                    "Whisper não instalado. Execute: pip install openai-whisper"
                )
                raise
        return self.model

    def transcribe_audio(self, audio_path: str, language: Optional[str] = "pt") -> str:
        """
        Transcreve arquivo de áudio para texto
        """
        try:
            # Carregar modelo
            model = self.load_model()

            # Transcrição
            result = model.transcribe(
                audio_path, language=language, fp16=(self.device == "cuda")
            )

            if result and "text" in result and isinstance(result["text"], str):
                return result["text"].strip()
            else:
                return ""
        except Exception as e:
            logger.error(f"Falha na transcrição: {str(e)}")
            return ""

    def convert_to_wav(self, input_path: str) -> str:
        """Converte arquivo para WAV temporário"""
        output_path = tempfile.mktemp(suffix=".wav")

        try:
            import ffmpeg  # type: ignore

            (
                ffmpeg.input(input_path)
                .output(output_path, ar="16000", ac=1)
                .run(quiet=True, overwrite_output=True)
            )
            return output_path
        except Exception as e:
            logger.error(f"Erro na conversão de áudio: {e}")
            # Se FFmpeg falhar, tenta usar o arquivo original
            return input_path

    @staticmethod
    def transcribe_file(audio_path: str) -> str:
        """Método estático para uso rápido"""
        service = AudioTranscriptionService()
        return service.transcribe_audio(audio_path)
