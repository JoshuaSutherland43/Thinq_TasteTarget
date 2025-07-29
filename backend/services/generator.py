from fastapi import APIRouter, HTTPException
from datetime import datetime
from core.configuration.config import settings
from services.openai_service import call_openai_api, extract_json_from_response
from models.schemas import ProductInput, TasteTargetResponse, TastePersona, CampaignCopy
from services.qloo_service import call_qloo_api
from typing import List, Dict, Optional, Union, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate-targeting", response_model=TasteTargetResponse)
async def generate_targeting(product_input: ProductInput):
    try:
        taste_clusters = await call_qloo_api(product_input.dict())
        personas = await generate_personas_with_openai(product_input, taste_clusters)
        campaign_copies = await generate_campaign_copy_with_openai(
            product_input, personas
        )
        suggestions = await generate_suggestions(product_input, personas)

        return TasteTargetResponse(
            product_name=product_input.product_name,
            personas=personas,
            campaign_copies=campaign_copies,
            generation_timestamp=datetime.utcnow().isoformat(),
            suggestions=suggestions,
            data_source=(
                "Qloo Taste AI + OpenAI GPT-4"
                if settings.QLOO_API_KEY
                else "OpenAI GPT-4 (Mock Qloo)"
            ),
        )

    except Exception as e:
        logger.error(f"Error generating targeting: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to generate targeting insights"
        )


# Persona Generation with OpenAI
async def generate_personas_with_openai(
    product_input: ProductInput, taste_clusters: List[dict]
) -> List[TastePersona]:
    """Generate personas using OpenAI GPT-4"""
    personas = []

    for i, cluster in enumerate(taste_clusters):
        interests_summary = []
        for category, items in cluster["interests"].items():
            interests_summary.append(f"{category}: {', '.join(items[:3])}")

        prompt = f"""Create a detailed marketing persona for {product_input.product_name}.

Product: {product_input.product_description}
Brand values: {', '.join(product_input.brand_values)}
Cultural interests from data: {'; '.join(interests_summary)}

Generate a JSON object with exactly these fields:
{{
  "persona_name": "Creative 2-3 word name that captures their essence",
  "description": "2-3 sentence description of who they are and what drives them",
  "psychographics": ["trait1", "trait2", "trait3", "trait4", "trait5"],
  "preferred_channels": ["channel1", "channel2", "channel3", "channel4"],
  "influencer_types": ["type1", "type2", "type3"]
}}

Important: Return ONLY the JSON object, no other text or markdown."""

        try:
            response = await call_openai_api(prompt, temperature=0.7)
            persona_data = extract_json_from_response(response)

            if persona_data and "persona_name" in persona_data:
                personas.append(
                    TastePersona(
                        persona_id=cluster["cluster_id"],
                        name=persona_data.get("persona_name", f"Persona {i+1}"),
                        description=persona_data.get(
                            "description", "A key customer segment"
                        ),
                        cultural_interests=cluster["interests"],
                        psychographics=persona_data.get(
                            "psychographics", ["innovative", "conscious", "modern"]
                        ),
                        preferred_channels=persona_data.get(
                            "preferred_channels", ["Instagram", "Email", "YouTube"]
                        ),
                        influencer_types=persona_data.get(
                            "influencer_types", ["Micro-influencers", "Experts"]
                        ),
                    )
                )
                logger.info(
                    f"Successfully generated persona: {persona_data.get('persona_name')}"
                )
            else:
                raise ValueError("Invalid persona data from OpenAI")

        except Exception as e:
            logger.error(f"Persona generation error: {e}")
            personas.append(create_fallback_persona(cluster, i))

    return personas


def create_fallback_persona(cluster: dict, index: int) -> TastePersona:
    """Fallback persona when generation fails"""
    names = {
        "eco_conscious": "The Conscious Pioneer",
        "tech_innovator": "The Digital Explorer",
        "premium_lifestyle": "The Luxury Connoisseur",
        "balanced_modern": "The Modern Optimizer",
    }

    return TastePersona(
        persona_id=cluster["cluster_id"],
        name=names.get(cluster["cluster_id"], f"Persona {index + 1}"),
        description="A discerning customer who values quality and authenticity in their choices.",
        cultural_interests=cluster["interests"],
        psychographics=[
            "thoughtful",
            "quality-focused",
            "authentic",
            "curious",
            "trendsetting",
        ],
        preferred_channels=["Instagram", "Newsletter", "YouTube", "LinkedIn"],
        influencer_types=["Industry experts", "Lifestyle creators", "Thought leaders"],
    )


async def generate_campaign_copy_with_openai(
    product_input: ProductInput, personas: List[TastePersona]
) -> List[CampaignCopy]:
    """Generate campaign copy using OpenAI"""
    copies = []

    tone_guide = {
        "minimal": "Use few words, be direct and impactful",
        "balanced": "Professional yet approachable tone",
        "expressive": "Creative and emotionally engaging",
        "bold": "Strong statements and confident messaging",
    }

    for persona in personas:
        prompt = f"""Create marketing copy for {product_input.product_name} targeting {persona.name}.

Product: {product_input.product_description}
Customer Profile: {persona.description}
Their interests include: {', '.join(persona.cultural_interests.get('music', [])[:2])} music, {', '.join(persona.cultural_interests.get('fashion', [])[:2])} fashion
Tone: {product_input.campaign_tone} - {tone_guide.get(product_input.campaign_tone, 'balanced')}

Generate a JSON object with exactly these fields:
{{
  "tagline": "Maximum 8 words, memorable and impactful",
  "social_caption": "2-3 sentences for Instagram/TikTok with relevant emojis that speak to their interests",
  "ad_copy": "3-4 compelling sentences for display advertising",
  "email_subject": "Under 50 characters, creates curiosity",
  "product_description": "2-3 benefit-focused sentences tailored to this persona"
}}

Important: Return ONLY the JSON object, no other text or markdown."""

        try:
            response = await call_openai_api(prompt, temperature=0.8)
            copy_data = extract_json_from_response(response)

            if copy_data and "tagline" in copy_data:
                copies.append(
                    CampaignCopy(
                        persona_id=persona.persona_id,
                        tagline=copy_data.get("tagline", "Experience the difference"),
                        social_caption=copy_data.get(
                            "social_caption",
                            f"Discover {product_input.product_name} ✨",
                        ),
                        ad_copy=copy_data.get(
                            "ad_copy", "Transform your everyday experience."
                        ),
                        email_subject=copy_data.get(
                            "email_subject", "Something special awaits"
                        ),
                        product_description=copy_data.get(
                            "product_description", product_input.product_description
                        ),
                    )
                )
                logger.info(f"Successfully generated copy for: {persona.name}")
            else:
                raise ValueError("Invalid copy data from OpenAI")

        except Exception as e:
            logger.error(f"Copy generation error: {e}")
            copies.append(create_fallback_copy(product_input, persona))

    return copies


def create_fallback_copy(
    product_input: ProductInput, persona: TastePersona
) -> CampaignCopy:
    """Fallback copy when generation fails"""
    return CampaignCopy(
        persona_id=persona.persona_id,
        tagline=f"{product_input.product_name} - Crafted for You",
        social_caption=f"Meet {product_input.product_name} ✨ Where {product_input.brand_values[0] if product_input.brand_values else 'innovation'} meets style. Join our community! 🌟",
        ad_copy=f"Discover {product_input.product_name}. Thoughtfully designed for those who value {', '.join(product_input.brand_values[:2]) if product_input.brand_values else 'quality and innovation'}.",
        email_subject=f"Introducing {product_input.product_name[:30]}",
        product_description=f"{product_input.product_name} is more than a product - it's a statement of your values. {product_input.product_description}",
    )


async def generate_suggestions(
    product_input: ProductInput, personas: List[TastePersona]
) -> Dict[str, List[str]]:
    """Generate marketing suggestions based on personas and their interests"""
    all_interests = {}
    for persona in personas:
        for category, interests in persona.cultural_interests.items():
            if category not in all_interests:
                all_interests[category] = set()
            all_interests[category].update(interests)

    # Get top interests
    top_music = list(all_interests.get("music", []))[:2]
    top_fashion = list(all_interests.get("fashion", []))[:2]
    top_dining = list(all_interests.get("dining", []))[:2]

    suggestions = {
        "content_themes": [
            f"Behind the {product_input.product_name} story",
            "Customer spotlight: Real stories, real impact",
            f"The {product_input.brand_values[0] if product_input.brand_values else 'innovation'} guide",
            "Day in the life with our products",
        ],
        "partnership_ideas": [
            f"Collaborate with {top_music[0] if top_music else 'indie'} music artists",
            f"Partner with {top_fashion[0] if top_fashion else 'sustainable'} fashion brands",
            f"Pop-ups at {top_dining[0] if top_dining else 'local'} venues",
            "Co-create with cultural tastemakers",
        ],
        "campaign_angles": [
            f"The {product_input.brand_values[0] if product_input.brand_values else 'future'} starts here",
            "Join the movement",
            "Elevate your everyday",
            "Where values meet style",
        ],
        "visual_directions": [
            "Minimalist product photography",
            "Lifestyle shots in natural settings",
            "User-generated content campaigns",
            "Bold typography with clean layouts",
        ],
    }

    return suggestions
