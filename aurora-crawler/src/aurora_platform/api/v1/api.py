from fastapi import APIRouter

# --- CORREÇÃO: Removido o subdiretório '.endpoints' do caminho ---
try:
    from .endpoints.cnpj_router import cnpj_router
except ImportError:
    cnpj_router = None
try:
    from .endpoints.code_assist_router import code_assist_router
except ImportError:
    code_assist_router = None
try:
    from .endpoints.ai_log_router import ai_log_router
except ImportError:
    ai_log_router = None

api_router = APIRouter()

# Inclui os roteadores na API principal da v1, se existirem
if cnpj_router:
    api_router.include_router(cnpj_router, prefix="/cnpj", tags=["CNPJ"])
if code_assist_router:
    api_router.include_router(code_assist_router)
if ai_log_router:
    api_router.include_router(ai_log_router, prefix="/ia", tags=["AI Monitoring"])
