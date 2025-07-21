import asyncio
import json
from openai import OpenAI
from fastapi import HTTPException
from core.configuration.config import settings
import logging

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def call_openai_api(prompt: str, temperature: float = 0.7, model: str = "gpt-4o-mini") -> str:
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[
                {"role": "system", "content": "You are a marketing expert..."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def extract_json_from_response(response: str) -> dict:
    try:
        response = response.strip().lstrip("```json").lstrip("```").rstrip("```")
        return json.loads(response[response.find('{'):response.rfind('}')+1])
    except Exception as e:
        logger.warning(f"JSON parse error: {e}")
        return {}
