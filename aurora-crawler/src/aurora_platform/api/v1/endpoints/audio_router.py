import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from aurora_platform.services.audio_transcription_service import (
    AudioTranscriptionService,
)
from aurora_platform.services.knowledge_service import KnowledgeBaseService

router = APIRouter()


class TranscribeAndIngestRequest(BaseModel):
    title: str = "Audio Transcription"
    source: str = "audio_upload"
    collection_name: str = "default_knowledge_base"


def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcrever arquivo de áudio"""
    if not file.filename or not file.filename.lower().endswith(
        (".opus", ".mp3", ".wav", ".m4a", ".ogg")
    ):
        raise HTTPException(status_code=400, detail="Formato de áudio não suportado")

    temp_path = None
    try:
        # Salvar arquivo temporário
        suffix = (
            os.path.splitext(file.filename or ".tmp")[1] if file.filename else ".tmp"
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            content = await file.read()
            temp_audio.write(content)
            temp_path = temp_audio.name

        # Transcrever
        service = AudioTranscriptionService()
        transcription = service.transcribe_audio(temp_path)

        if not transcription:
            raise HTTPException(
                status_code=422, detail="Não foi possível transcrever o áudio"
            )

        return JSONResponse(
            content={
                "status": "success",
                "transcription": transcription,
                "filename": file.filename,
                "model": "whisper-tiny",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na transcrição: {str(e)}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post("/transcribe-and-ingest")
async def transcribe_and_ingest(
    file: UploadFile = File(...),
    metadata: TranscribeAndIngestRequest = TranscribeAndIngestRequest(),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """Transcrever áudio e ingerir na base de conhecimento"""
    if not file.filename or not file.filename.lower().endswith(
        (".opus", ".mp3", ".wav", ".m4a", ".ogg")
    ):
        raise HTTPException(status_code=400, detail="Formato de áudio não suportado")

    temp_path = None
    try:
        # Salvar arquivo temporário
        suffix = (
            os.path.splitext(file.filename or ".tmp")[1] if file.filename else ".tmp"
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            content = await file.read()
            temp_audio.write(content)
            temp_path = temp_audio.name

        # Transcrever
        service = AudioTranscriptionService()
        transcription = service.transcribe_audio(temp_path)

        if not transcription:
            raise HTTPException(
                status_code=422, detail="Não foi possível transcrever o áudio"
            )

        # Ingerir na base de conhecimento
        doc_id = f"audio_{file.filename}_{hash(transcription) % 10000}"
        doc_metadata = {
            "source": metadata.source,
            "title": metadata.title,
            "filename": file.filename,
            "type": "audio_transcription",
        }

        kb_service.add_document(
            doc_id,
            transcription,
            doc_metadata,
            collection_name=metadata.collection_name,
        )

        return JSONResponse(
            content={
                "status": "success",
                "transcription": transcription,
                "document_id": doc_id,
                "ingested": True,
                "filename": file.filename,
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro na transcrição e ingestão: {str(e)}"
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
