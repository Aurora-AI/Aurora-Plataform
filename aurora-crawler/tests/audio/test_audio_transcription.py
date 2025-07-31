import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_audio_service():
    """Testa o serviço de transcrição de áudio"""
    try:
        from aurora_platform.services.audio_transcription_service import (
            AudioTranscriptionService,
        )

        service = AudioTranscriptionService()
        print("OK AudioTranscriptionService importado com sucesso")

        # Teste de carregamento do modelo (sem arquivo)
        try:
            model = service.load_model()
            print("OK Modelo Whisper carregado com sucesso")
            assert True
        except Exception as e:
            print(f"AVISO: Modelo Whisper não disponível: {e}")
            print("Execute: pip install openai-whisper")
            assert False

    except Exception as e:
        print(f"ERRO no AudioTranscriptionService: {e}")
        assert False


def test_audio_api():
    """Testa se a API de áudio foi registrada"""
    try:
        from aurora_platform.api.v1.endpoints.audio_router import router

        print("OK Audio router importado com sucesso")
        print(f"OK Endpoints disponíveis: {len(router.routes)} rotas")
        assert True
    except Exception as e:
        print(f"ERRO no audio router: {e}")
        assert False


if __name__ == "__main__":
    print("TESTE AUDIO TRANSCRIPTION - Aurora Platform\n")

    print("1. Testando AudioTranscriptionService...")
    service_ok = test_audio_service()

    print("\n2. Testando Audio API...")
    api_ok = test_audio_api()

    print(f"\nResultados:")
    print(f"AudioService: {'OK' if service_ok else 'FALHOU'}")
    print(f"Audio API: {'OK' if api_ok else 'FALHOU'}")

    if service_ok and api_ok:
        print("\nSistema de audio pronto!")
        print("Execute: python run.py")
        print("Acesse: http://localhost:8001/docs")
    else:
        print("\nInstale dependencias: pip install openai-whisper ffmpeg-python")
