from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import json
import httpx
from datetime import datetime
import logging
import asyncio
import re

# Load environment variables
load_dotenv()

# API Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
QLOO_API_KEY = os.getenv("QLOO_API_KEY")
QLOO_API_URL = os.getenv("QLOO_API_URL", "https://hackathon.api.qloo.com")

# Hugging Face Models
MODELS = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.3",
    "flan": "google/flan-t5-large",
    "zephyr": "HuggingFaceH4/zephyr-7b-beta"  # Alternative to Mistral
}

# Select models for different tasks
PERSONA_MODEL = MODELS["mistral"]
COPY_MODEL = MODELS["mistral"]
FALLBACK_MODEL = MODELS["flan"]

HF_API_BASE = "https://api-inference.huggingface.co/models"

APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TasteTarget API - Qloo + HuggingFace",
    description="AI-Powered Cultural Targeting using Qloo's Taste AI and Open Source Models",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ProductInput(BaseModel):
    product_name: str = Field(..., example="Eco-Friendly Vegan Sneakers")
    product_description: str = Field(..., example="Minimalist design, sustainable materials, zero waste production")
    brand_values: List[str] = Field(default=[], example=["sustainability", "minimalism", "ethical"])
    target_mood: List[str] = Field(default=[], example=["conscious", "modern", "clean"])
    campaign_tone: str = Field(default="balanced", example="balanced")

class TastePersona(BaseModel):
    persona_id: str
    name: str
    description: str
    cultural_interests: Dict[str, List[str]]
    psychographics: List[str]
    preferred_channels: List[str]
    influencer_types: List[str]

class CampaignCopy(BaseModel):
    persona_id: str
    tagline: str
    social_caption: str
    ad_copy: str
    email_subject: str
    product_description: str

class TasteTargetResponse(BaseModel):
    product_name: str
    personas: List[TastePersona]
    campaign_copies: List[CampaignCopy]
    generation_timestamp: str
    suggestions: Dict[str, List[str]]
    data_source: str = Field(default="Qloo Taste AI + HuggingFace")

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    qloo_connected: bool
    huggingface_connected: bool

# Qloo API Integration
async def call_qloo_api(product_info: dict) -> List[dict]:
    """
    Call Qloo API for taste-based insights
    """
    if not QLOO_API_KEY:
        logger.warning("QLOO_API_KEY not found, using mock data")
        return await mock_qloo_api(product_info)
    
    headers = {
        "x-api-key": QLOO_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Prepare the search query based on product info
    search_query = f"{product_info.get('product_name', '')} {' '.join(product_info.get('brand_values', []))}"
    
    # Try multiple Qloo endpoints to get taste data
    clusters = []
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Try to get taste data for the product category
            # Note: Adjust these endpoints based on Qloo's actual API documentation
            
            # Example: Search for similar entities
            search_payload = {
                "query": search_query,
                "limit": 5
            }
            
            # Try entity search
            try:
                response = await client.post(
                    f"{QLOO_API_URL}/search",
                    headers=headers,
                    json=search_payload
                )
                if response.status_code == 200:
                    search_results = response.json()
                    logger.info(f"Qloo search returned: {search_results}")
            except Exception as e:
                logger.error(f"Qloo search error: {e}")
            
            # Try to get taste correlations
            # This is a hypothetical endpoint - adjust based on actual Qloo API
            for value in product_info.get('brand_values', [])[:2]:
                try:
                    correlation_payload = {
                        "entity": value,
                        "category": "lifestyle"
                    }
                    
                    response = await client.post(
                        f"{QLOO_API_URL}/correlations",
                        headers=headers,
                        json=correlation_payload
                    )
                    
                    if response.status_code == 200:
                        correlations = response.json()
                        # Convert Qloo data to our cluster format
                        cluster = convert_qloo_to_cluster(correlations, value)
                        if cluster:
                            clusters.append(cluster)
                            
                except Exception as e:
                    logger.error(f"Qloo correlation error for {value}: {e}")
                    
    except Exception as e:
        logger.error(f"Qloo API error: {str(e)}")
    
    # If we got data from Qloo, use it; otherwise fall back to mock
    if clusters:
        logger.info(f"Successfully retrieved {len(clusters)} clusters from Qloo")
        return clusters
    else:
        logger.warning("No data from Qloo API, using mock data")
        return await mock_qloo_api(product_info)

def convert_qloo_to_cluster(qloo_data: dict, cluster_name: str) -> dict:
    """Convert Qloo API response to our cluster format"""
    try:
        # This is a hypothetical conversion - adjust based on actual Qloo response format
        return {
            "cluster_id": f"qloo_{cluster_name}",
            "interests": {
                "music": qloo_data.get("music", ["indie", "alternative", "electronic"])[:5],
                "reading": qloo_data.get("books", ["contemporary fiction", "non-fiction", "blogs"])[:5],
                "dining": qloo_data.get("dining", ["local cuisine", "cafes", "healthy food"])[:5],
                "travel": qloo_data.get("travel", ["city breaks", "nature", "cultural sites"])[:5],
                "fashion": qloo_data.get("fashion", ["contemporary", "sustainable", "minimalist"])[:5]
            }
        }
    except Exception as e:
        logger.error(f"Error converting Qloo data: {e}")
        return None

async def mock_qloo_api(product_info: dict) -> List[dict]:
    """Fallback mock data when Qloo API is unavailable"""
    await asyncio.sleep(0.5)
    
    clusters = []
    
    # Generate clusters based on brand values
    if "sustainability" in product_info.get("brand_values", []) or "ethical" in product_info.get("brand_values", []):
        clusters.append({
            "cluster_id": "eco_conscious",
            "interests": {
                "music": ["indie folk", "acoustic", "world music", "nature sounds", "ambient"],
                "reading": ["environmental books", "sustainable living blogs", "philosophy", "poetry", "mindfulness"],
                "dining": ["farm-to-table", "vegan restaurants", "organic cafes", "juice bars", "farmers markets"],
                "travel": ["eco-lodges", "national parks", "hiking trails", "sustainable tourism", "volunteer trips"],
                "fashion": ["sustainable brands", "vintage shops", "minimalist style", "natural fabrics", "ethical fashion"]
            }
        })
    
    if "innovation" in product_info.get("brand_values", []) or "modern" in product_info.get("brand_values", []):
        clusters.append({
            "cluster_id": "tech_innovator",
            "interests": {
                "music": ["electronic", "synthwave", "experimental", "techno", "future bass"],
                "reading": ["tech blogs", "sci-fi novels", "innovation magazines", "startup stories", "futurism"],
                "dining": ["trendy restaurants", "food tech", "molecular gastronomy", "pop-ups", "delivery apps"],
                "travel": ["smart cities", "tech hubs", "conferences", "urban exploration", "digital nomad spots"],
                "fashion": ["techwear", "designer collaborations", "smart accessories", "limited editions", "streetwear"]
            }
        })
    
    if "luxury" in product_info.get("brand_values", []) or "quality" in product_info.get("brand_values", []):
        clusters.append({
            "cluster_id": "premium_lifestyle",
            "interests": {
                "music": ["jazz", "classical", "lounge", "live performances", "exclusive venues"],
                "reading": ["luxury magazines", "art books", "biographies", "investment guides", "wine publications"],
                "dining": ["fine dining", "michelin restaurants", "wine bars", "private clubs", "chef's table"],
                "travel": ["luxury resorts", "private jets", "exclusive destinations", "cultural capitals", "yacht trips"],
                "fashion": ["haute couture", "designer brands", "bespoke tailoring", "luxury accessories", "timeless pieces"]
            }
        })
    
    # Always add a balanced lifestyle cluster
    if len(clusters) < 3:
        clusters.append({
            "cluster_id": "balanced_modern",
            "interests": {
                "music": ["pop", "indie", "podcasts", "spotify playlists", "live music"],
                "reading": ["bestsellers", "online articles", "lifestyle blogs", "self-help", "newsletters"],
                "dining": ["trendy cafes", "brunch spots", "food delivery", "local favorites", "social dining"],
                "travel": ["weekend trips", "city breaks", "instagram spots", "airbnb", "group travel"],
                "fashion": ["contemporary brands", "online shopping", "seasonal trends", "athleisure", "accessories"]
            }
        })
    
    return clusters[:3]

# Hugging Face Integration
async def call_huggingface_api(
    prompt: str, 
    model: str = PERSONA_MODEL,
    max_tokens: int = 500, 
    temperature: float = 0.7,
    retry_with_fallback: bool = True
) -> str:
    """Call Hugging Face API with specified model"""
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format prompt based on model
    if "mistral" in model.lower() or "zephyr" in model.lower():
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
    else:
        formatted_prompt = prompt
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "do_sample": True,
            "return_full_text": False,
            "repetition_penalty": 1.1
        }
    }
    
    max_retries = 3
    current_model = model
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                api_url = f"{HF_API_BASE}/{current_model}"
                response = await client.post(api_url, headers=headers, json=payload)
                
                if response.status_code == 503:
                    logger.info(f"Model {current_model} loading, waiting 20 seconds...")
                    await asyncio.sleep(20)
                    continue
                
                if response.status_code != 200:
                    logger.error(f"API returned {response.status_code}: {response.text}")
                    if retry_with_fallback and current_model != FALLBACK_MODEL:
                        logger.info(f"Switching to fallback model: {FALLBACK_MODEL}")
                        current_model = FALLBACK_MODEL
                        continue
                
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    return clean_response(result[0].get("generated_text", ""))
                elif isinstance(result, dict) and "generated_text" in result:
                    return clean_response(result["generated_text"])
                    
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(5)
                continue
    
    raise HTTPException(status_code=500, detail="Failed to generate content")

def clean_response(text: str) -> str:
    """Clean up model response"""
    text = re.sub(r'<s>|</s>|\[INST\]|\[/INST\]', '', text)
    return ' '.join(text.split()).strip()

def extract_json_from_response(response: str) -> dict:
    """Extract JSON from model response"""
    try:
        response = response.strip()
        
        # Find JSON in response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = response[json_start:json_end]
            json_str = json_str.replace("'", '"')
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            return json.loads(json_str)
        
        return json.loads(response)
        
    except Exception as e:
        logger.warning(f"JSON parse error: {e}")
        return {}

# Persona and Copy Generation
async def generate_personas_with_hf(product_input: ProductInput, taste_clusters: List[dict]) -> List[TastePersona]:
    """Generate personas using Hugging Face"""
    personas = []
    
    for i, cluster in enumerate(taste_clusters):
        interests_summary = []
        for category, items in cluster['interests'].items():
            interests_summary.append(f"{category}: {', '.join(items[:3])}")
        
        prompt = f"""Create a detailed marketing persona for {product_input.product_name}.

Product: {product_input.product_description}
Brand values: {', '.join(product_input.brand_values)}
Cultural interests: {'; '.join(interests_summary)}

Generate a JSON with:
{{
  "persona_name": "Creative 2-3 word name",
  "description": "2-3 sentence description",
  "psychographics": ["trait1", "trait2", "trait3", "trait4", "trait5"],
  "preferred_channels": ["channel1", "channel2", "channel3", "channel4"],
  "influencer_types": ["type1", "type2", "type3"]
}}

Return only JSON, no other text."""

        try:
            response = await call_huggingface_api(prompt, temperature=0.7)
            persona_data = extract_json_from_response(response)
            
            if persona_data and "persona_name" in persona_data:
                personas.append(TastePersona(
                    persona_id=cluster['cluster_id'],
                    name=persona_data.get('persona_name', f'Persona {i+1}'),
                    description=persona_data.get('description', 'A key customer segment'),
                    cultural_interests=cluster['interests'],
                    psychographics=persona_data.get('psychographics', ['innovative', 'conscious', 'modern']),
                    preferred_channels=persona_data.get('preferred_channels', ['Instagram', 'Email', 'YouTube']),
                    influencer_types=persona_data.get('influencer_types', ['Micro-influencers', 'Experts'])
                ))
            else:
                raise ValueError("Invalid persona data")
                
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
        "balanced_modern": "The Modern Optimizer"
    }
    
    return TastePersona(
        persona_id=cluster['cluster_id'],
        name=names.get(cluster['cluster_id'], f"Persona {index + 1}"),
        description="A discerning customer who values quality and authenticity in their choices.",
        cultural_interests=cluster['interests'],
        psychographics=["thoughtful", "quality-focused", "authentic", "curious", "trendsetting"],
        preferred_channels=["Instagram", "Newsletter", "YouTube", "LinkedIn"],
        influencer_types=["Industry experts", "Lifestyle creators", "Thought leaders"]
    )

async def generate_campaign_copy_with_hf(product_input: ProductInput, personas: List[TastePersona]) -> List[CampaignCopy]:
    """Generate campaign copy using Hugging Face"""
    copies = []
    
    for persona in personas:
        prompt = f"""Create marketing copy for {product_input.product_name} targeting {persona.name}.

Product: {product_input.product_description}
Customer: {persona.description}
Tone: {product_input.campaign_tone}

Generate JSON:
{{
  "tagline": "Max 8 words",
  "social_caption": "2-3 sentences with emojis",
  "ad_copy": "3-4 compelling sentences",
  "email_subject": "Under 50 characters",
  "product_description": "2-3 benefit-focused sentences"
}}

Return only JSON."""

        try:
            response = await call_huggingface_api(prompt, temperature=0.8)
            copy_data = extract_json_from_response(response)
            
            if copy_data and "tagline" in copy_data:
                copies.append(CampaignCopy(
                    persona_id=persona.persona_id,
                    tagline=copy_data.get('tagline', 'Experience the difference'),
                    social_caption=copy_data.get('social_caption', f'Discover {product_input.product_name} ✨'),
                    ad_copy=copy_data.get('ad_copy', 'Transform your everyday experience.'),
                    email_subject=copy_data.get('email_subject', 'Something special awaits'),
                    product_description=copy_data.get('product_description', product_input.product_description)
                ))
            else:
                raise ValueError("Invalid copy data")
                
        except Exception as e:
            logger.error(f"Copy generation error: {e}")
            copies.append(create_fallback_copy(product_input, persona))
    
    return copies

def create_fallback_copy(product_input: ProductInput, persona: TastePersona) -> CampaignCopy:
    """Fallback copy when generation fails"""
    return CampaignCopy(
        persona_id=persona.persona_id,
        tagline=f"{product_input.product_name} - Crafted for You",
        social_caption=f"Meet {product_input.product_name} ✨ Where {product_input.brand_values[0] if product_input.brand_values else 'innovation'} meets style. Join our community! 🌟",
        ad_copy=f"Discover {product_input.product_name}. Thoughtfully designed for those who value {', '.join(product_input.brand_values[:2]) if product_input.brand_values else 'quality and innovation'}.",
        email_subject=f"Introducing {product_input.product_name[:30]}",
        product_description=f"{product_input.product_name} is more than a product - it's a statement of your values. {product_input.product_description}"
    )

async def generate_suggestions(product_input: ProductInput, personas: List[TastePersona]) -> Dict[str, List[str]]:
    """Generate marketing suggestions"""
    all_interests = {}
    for persona in personas:
        for category, interests in persona.cultural_interests.items():
            if category not in all_interests:
                all_interests[category] = set()
            all_interests[category].update(interests)
    
    # Get top interests
    top_music = list(all_interests.get('music', []))[:2]
    top_fashion = list(all_interests.get('fashion', []))[:2]
    
    suggestions = {
        "content_themes": [
            f"Behind the {product_input.product_name} story",
            "Customer spotlight: Real stories, real impact",
            f"The {product_input.brand_values[0] if product_input.brand_values else 'innovation'} guide",
            "Day in the life with our products"
        ],
        "partnership_ideas": [
            f"Collaborate with {top_music[0] if top_music else 'indie'} music artists",
            f"Partner with {top_fashion[0] if top_fashion else 'sustainable'} fashion brands",
            "Sponsor cultural events and pop-ups",
            "Co-create with local artisans"
        ],
        "campaign_angles": [
            f"The {product_input.brand_values[0] if product_input.brand_values else 'future'} is now",
            "Join the conscious revolution",
            "Elevate your everyday",
            "Where purpose meets passion"
        ],
        "visual_directions": [
            "Minimalist product photography",
            "Lifestyle shots in natural settings",
            "User-generated content focus",
            "Bold typography with clean aesthetics"
        ]
    }
    
    return suggestions

# API Endpoints
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Test connections
    qloo_connected = bool(QLOO_API_KEY)
    hf_connected = bool(HUGGINGFACE_API_KEY)
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="2.0.0",
        qloo_connected=qloo_connected,
        huggingface_connected=hf_connected
    )

@app.post("/api/generate-targeting", response_model=TasteTargetResponse)
async def generate_targeting(product_input: ProductInput):
    """Generate taste-based targeting using Qloo + HuggingFace"""
    try:
        logger.info(f"Generating targeting for: {product_input.product_name}")
        logger.info(f"Using Qloo API: {bool(QLOO_API_KEY)}")
        
        # Step 1: Get taste clusters from Qloo API
        taste_clusters = await call_qloo_api(product_input.dict())
        logger.info(f"Retrieved {len(taste_clusters)} taste clusters")
        
        # Step 2: Generate personas using HuggingFace
        personas = await generate_personas_with_hf(product_input, taste_clusters)
        logger.info(f"Generated {len(personas)} personas")
        
        # Step 3: Generate campaign copy
        campaign_copies = await generate_campaign_copy_with_hf(product_input, personas)
        logger.info(f"Generated {len(campaign_copies)} copy variations")
        
        # Step 4: Generate suggestions
        suggestions = await generate_suggestions(product_input, personas)
        
        # Determine data source
        data_source = "Qloo Taste AI + HuggingFace" if QLOO_API_KEY else "HuggingFace (Mock Qloo Data)"
        
        response = TasteTargetResponse(
            product_name=product_input.product_name,
            personas=personas,
            campaign_copies=campaign_copies,
            generation_timestamp=datetime.utcnow().isoformat(),
            suggestions=suggestions,
            data_source=data_source
        )
        
        logger.info(f"Successfully generated targeting for: {product_input.product_name}")
        return response
        
    except Exception as e:
        logger.error(f"Error in generate_targeting: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test-connections")
async def test_connections():
    """Test API connections"""
    results = {
        "qloo": {"configured": bool(QLOO_API_KEY), "status": "unknown"},
        "huggingface": {"configured": bool(HUGGINGFACE_API_KEY), "status": "unknown"}
    }
    
    # Test Qloo
    if QLOO_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    QLOO_API_URL,
                    headers={"x-api-key": QLOO_API_KEY}
                )
                results["qloo"]["status"] = "connected" if response.status_code < 500 else "error"
        except:
            results["qloo"]["status"] = "error"
    
    # Test HuggingFace
    if HUGGINGFACE_API_KEY:
        try:
            response = await call_huggingface_api(
                "Test connection",
                model=FALLBACK_MODEL,
                max_tokens=10
            )
            results["huggingface"]["status"] = "connected" if response else "error"
        except:
            results["huggingface"]["status"] = "error"
    
    return results

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting TasteTarget API with Qloo + HuggingFace...")
    logger.info(f"Qloo API: {'Connected' if QLOO_API_KEY else 'Not configured'}")
    logger.info(f"HuggingFace API: {'Connected' if HUGGINGFACE_API_KEY else 'Not configured'}")
    uvicorn.run(app, host="0.0.0.0", port=8000)