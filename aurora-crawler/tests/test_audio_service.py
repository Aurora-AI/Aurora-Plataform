"""Testes para AudioTranscriptionService"""

import pytest
from aurora_platform.services.audio_transcription_service import (
    AudioTranscriptionService,
)


def test_audio_service_init():
    """Testa inicialização do serviço"""
    service = AudioTranscriptionService()
    assert service is not None
    assert service.device in ["cpu", "cuda"]


def test_load_model():
    """Testa carregamento do modelo (pode falhar se Whisper não estiver instalado)"""
    service = AudioTranscriptionService()
    try:
        model = service.load_model()
        assert model is not None
    except ImportError:
        pytest.skip("Whisper não instalado")


def test_static_method():
    """Testa método estático (sem arquivo real)"""
    # Este teste só verifica se o método existe
    assert hasattr(AudioTranscriptionService, "transcribe_file")
    assert callable(AudioTranscriptionService.transcribe_file)
