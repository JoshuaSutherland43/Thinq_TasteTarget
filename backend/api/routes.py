from fastapi import APIRouter, HTTPException
from models.schemas import ProductInput, TasteTargetResponse
from services.qloo_service import call_qloo_api
from services.generator import (
    generate_personas_with_openai,
    generate_campaign_copy_with_openai,
    generate_suggestions
)
from datetime import datetime
from core.configuration.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-targeting", response_model=TasteTargetResponse)
async def generate_targeting(product_input: ProductInput):
    try:
        taste_clusters = await call_qloo_api(product_input.dict())
        personas = await generate_personas_with_openai(product_input, taste_clusters)
        campaign_copies = await generate_campaign_copy_with_openai(product_input, personas)
        suggestions = await generate_suggestions(product_input, personas)

        return TasteTargetResponse(
            product_name=product_input.product_name,
            personas=personas,
            campaign_copies=campaign_copies,
            generation_timestamp=datetime.utcnow().isoformat(),
            suggestions=suggestions,
            data_source="Qloo Taste AI + OpenAI GPT-4" if settings.QLOO_API_KEY else "OpenAI GPT-4 (Mock Qloo)"
        )
    except Exception as e:
        logger.error(f"Error generating targeting: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
