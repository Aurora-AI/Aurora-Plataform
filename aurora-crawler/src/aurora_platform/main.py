from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from aurora_platform.api.v1.endpoints import (
    knowledge_router,
    audio_router,
    document_router,
    auth_router,
    etp_router,
    pipeline_router,
    summarize_router,
)
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        app.state.kb_service = KnowledgeBaseService()
        logger.info("KnowledgeBaseService initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize KnowledgeBaseService: {e}")
        raise
    yield
    # Shutdown
    logger.info("Application shutdown")


app = FastAPI(title="Aurora Platform", version="0.1.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Aurora-Core AIOS. O sistema está operacional."}


app.include_router(
    knowledge_router.router, prefix="/api/v1/knowledge", tags=["knowledge"]
)

app.include_router(audio_router.router, prefix="/api/v1/audio", tags=["audio"])

app.include_router(
    document_router.router, prefix="/api/v1/documents", tags=["documents"]
)

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])

app.include_router(etp_router.router, prefix="/api/v1/etp", tags=["etp"])


app.include_router(
    pipeline_router.router, prefix="/api/v1/pipelines", tags=["pipelines"]
)
app.include_router(
    summarize_router.router, prefix="/api/v1/browser", tags=["browser-automation"]
)
