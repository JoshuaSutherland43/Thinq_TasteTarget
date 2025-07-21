from fastapi import APIRouter
from models.schemas import HealthResponse
from datetime import datetime
from core.configuration.config import settings

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="3.0.0",
        qloo_connected=bool(settings.QLOO_API_KEY),
        openai_connected=bool(settings.OPENAI_API_KEY)
    )
