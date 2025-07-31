from fastapi import APIRouter, HTTPException, Depends
from aurora_platform.schemas.etp_schemas import ETPRequest
from aurora_platform.services.etp_generator_service import ETPGeneratorService
from aurora_platform.api.v1.endpoints.auth_router import get_current_user

router = APIRouter()


@router.post(
    "/generate",
    summary="Gera um Estudo Técnico Preliminar (ETP) usando RAG",
    response_model=dict,
)
async def generate_etp(
    request_body: ETPRequest, current_user: str = Depends(get_current_user)
):
    """
    Gera um Estudo Técnico Preliminar (ETP) em Markdown usando o serviço de RAG.
    """
    try:
        generator = ETPGeneratorService()
        etp_markdown = generator.generate_etp(request_body.topic)
        return {
            "status": "success",
            "message": "ETP gerado com sucesso",
            "etp_markdown": etp_markdown,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na geração ETP: {str(e)}")
