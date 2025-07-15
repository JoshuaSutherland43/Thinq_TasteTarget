from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import openai
import json
import httpx
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TasteTarget API",
    description="AI-Powered Cultural Targeting for Brands & Creators",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request/Response Models
class ProductInput(BaseModel):
    product_name: str = Field(..., example="Eco-Friendly Vegan Sneakers")
    product_description: str = Field(..., example="Minimalist design, sustainable materials, zero waste production")
    brand_values: List[str] = Field(default=[], example=["sustainability", "minimalism", "ethical"])
    target_mood: List[str] = Field(default=[], example=["conscious", "modern", "clean"])
    campaign_tone: str = Field(default="balanced", example="balanced")  # poetic, bold, humorous, balanced

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

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# Utility Functions
async def mock_qloo_api(product_info: dict) -> List[dict]:
    """
    Mock Qloo API response for taste-based personas
    In production, this would call the actual Qloo API
    """
    # Simulate API delay
    import asyncio
    await asyncio.sleep(0.5)
    
    # Return mock taste clusters
    return [
        {
            "cluster_id": "indie_conscious",
            "interests": {
                "music": ["indie folk", "lo-fi hip hop", "acoustic"],
                "reading": ["Murakami", "sustainability blogs", "minimalist philosophy"],
                "dining": ["farm-to-table", "vegan cafes", "matcha bars"],
                "travel": ["eco-lodges", "hiking trails", "cultural immersion"],
                "fashion": ["vintage", "sustainable brands", "minimalist aesthetic"]
            }
        },
        {
            "cluster_id": "urban_creative",
            "interests": {
                "music": ["electronic", "afrobeats", "jazz fusion"],
                "reading": ["design magazines", "tech blogs", "street art books"],
                "dining": ["fusion cuisine", "coffee culture", "food trucks"],
                "travel": ["city breaks", "art galleries", "music festivals"],
                "fashion": ["streetwear", "upcycled fashion", "bold accessories"]
            }
        },
        {
            "cluster_id": "wellness_warrior",
            "interests": {
                "music": ["meditation sounds", "nature recordings", "yoga playlists"],
                "reading": ["wellness journals", "mindfulness books", "nutrition guides"],
                "dining": ["organic restaurants", "juice bars", "plant-based cuisine"],
                "travel": ["wellness retreats", "nature escapes", "spiritual journeys"],
                "fashion": ["athleisure", "natural fibers", "comfortable minimalism"]
            }
        }
    ]

async def generate_personas_with_gpt(product_input: ProductInput, taste_clusters: List[dict]) -> List[TastePersona]:
    """Generate detailed personas using GPT-4"""
    personas = []
    
    for cluster in taste_clusters:
        prompt = f"""
        Based on this taste cluster and product, create a detailed marketing persona:
        
        Product: {product_input.product_name}
        Description: {product_input.product_description}
        Brand Values: {', '.join(product_input.brand_values)}
        
        Taste Cluster Interests:
        {json.dumps(cluster['interests'], indent=2)}
        
        Generate a JSON response with:
        1. persona_name (creative, memorable name)
        2. description (2-3 sentences about who they are)
        3. psychographics (5 personality traits/values)
        4. preferred_channels (top 3-4 marketing channels)
        5. influencer_types (3 types of influencers they follow)
        
        Make it specific and actionable for marketing teams.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a cultural intelligence expert helping brands understand their audiences through taste-based targeting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            persona_data = json.loads(response.choices[0].message.content)
            
            personas.append(TastePersona(
                persona_id=cluster['cluster_id'],
                name=persona_data['persona_name'],
                description=persona_data['description'],
                cultural_interests=cluster['interests'],
                psychographics=persona_data['psychographics'],
                preferred_channels=persona_data['preferred_channels'],
                influencer_types=persona_data['influencer_types']
            ))
            
        except Exception as e:
            logger.error(f"Error generating persona: {str(e)}")
            # Fallback persona
            personas.append(TastePersona(
                persona_id=cluster['cluster_id'],
                name=f"Cultural Explorer {len(personas) + 1}",
                description="A culturally aware consumer who values authenticity and sustainability.",
                cultural_interests=cluster['interests'],
                psychographics=["conscious", "creative", "authentic", "curious", "values-driven"],
                preferred_channels=["Instagram", "TikTok", "Newsletters", "Podcasts"],
                influencer_types=["Micro-influencers", "Thought leaders", "Artists"]
            ))
    
    return personas

async def generate_campaign_copy(product_input: ProductInput, personas: List[TastePersona]) -> List[CampaignCopy]:
    """Generate personalized campaign copy for each persona"""
    copies = []
    
    tone_instructions = {
        "poetic": "Use metaphorical, emotional, and artistic language",
        "bold": "Be direct, confident, and impactful with strong statements",
        "humorous": "Include wit, playfulness, and relatable humor",
        "balanced": "Mix professionalism with approachability and authenticity"
    }
    
    for persona in personas:
        prompt = f"""
        Create marketing copy for this specific audience persona:
        
        Product: {product_input.product_name}
        Description: {product_input.product_description}
        Brand Values: {', '.join(product_input.brand_values)}
        
        Target Persona: {persona.name}
        Description: {persona.description}
        Their Interests: {json.dumps(persona.cultural_interests, indent=2)}
        Psychographics: {', '.join(persona.psychographics)}
        
        Tone: {product_input.campaign_tone} - {tone_instructions.get(product_input.campaign_tone, '')}
        
        Generate:
        1. tagline (max 8 words, memorable)
        2. social_caption (Instagram/TikTok style, 2-3 sentences, include relevant emojis)
        3. ad_copy (3-4 sentences for display ads)
        4. email_subject (compelling, under 50 characters)
        5. product_description (2-3 sentences, persona-specific angle)
        
        Make each piece speak directly to this persona's values and interests.
        Return as JSON.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert copywriter who creates culturally-resonant marketing messages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=600
            )
            
            copy_data = json.loads(response.choices[0].message.content)
            
            copies.append(CampaignCopy(
                persona_id=persona.persona_id,
                tagline=copy_data['tagline'],
                social_caption=copy_data['social_caption'],
                ad_copy=copy_data['ad_copy'],
                email_subject=copy_data['email_subject'],
                product_description=copy_data['product_description']
            ))
            
        except Exception as e:
            logger.error(f"Error generating copy: {str(e)}")
            # Fallback copy
            copies.append(CampaignCopy(
                persona_id=persona.persona_id,
                tagline=f"{product_input.product_name} - Made for You",
                social_caption=f"Discover {product_input.product_name} 🌿 Designed with your values in mind. #Sustainable #Conscious",
                ad_copy=f"Meet {product_input.product_name}. Crafted for those who care about style and sustainability. Join the conscious movement.",
                email_subject="Your Perfect Match is Here",
                product_description=f"{product_input.product_name} combines timeless design with modern values. Perfect for the conscious consumer."
            ))
    
    return copies

async def generate_suggestions(product_input: ProductInput, personas: List[TastePersona]) -> Dict[str, List[str]]:
    """Generate additional marketing suggestions"""
    suggestions = {
        "content_themes": [],
        "partnership_ideas": [],
        "campaign_angles": [],
        "visual_directions": []
    }
    
    # Aggregate interests across personas
    all_interests = set()
    for persona in personas:
        for category, interests in persona.cultural_interests.items():
            all_interests.update(interests)
    
    # Generate contextual suggestions
    suggestions["content_themes"] = [
        "Behind-the-scenes: sustainable production process",
        "User stories: real customers living their values",
        "Educational: impact of conscious choices",
        "Lifestyle: integrating sustainability into daily life"
    ]
    
    suggestions["partnership_ideas"] = [
        "Collaborate with eco-conscious influencers",
        "Partner with sustainable lifestyle brands",
        "Sponsor local environmental initiatives",
        "Create limited editions with artists"
    ]
    
    suggestions["campaign_angles"] = [
        "The journey to zero waste",
        "Style meets sustainability",
        "Conscious choices, confident steps",
        "Walk the talk: values in action"
    ]
    
    suggestions["visual_directions"] = [
        "Natural lighting, outdoor settings",
        "Minimalist product photography",
        "User-generated content campaigns",
        "Before/after environmental impact visuals"
    ]
    
    return suggestions

# API Endpoints
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )

@app.post("/api/generate-targeting", response_model=TasteTargetResponse)
async def generate_targeting(product_input: ProductInput):
    """
    Main endpoint to generate taste-based targeting and campaign materials
    """
    try:
        logger.info(f"Generating targeting for: {product_input.product_name}")
        
        # Step 1: Get taste clusters (mock Qloo API)
        taste_clusters = await mock_qloo_api(product_input.dict())
        
        # Step 2: Generate detailed personas using GPT-4
        personas = await generate_personas_with_gpt(product_input, taste_clusters)
        
        # Step 3: Generate campaign copy for each persona
        campaign_copies = await generate_campaign_copy(product_input, personas)
        
        # Step 4: Generate additional suggestions
        suggestions = await generate_suggestions(product_input, personas)
        
        # Compile response
        response = TasteTargetResponse(
            product_name=product_input.product_name,
            personas=personas,
            campaign_copies=campaign_copies,
            generation_timestamp=datetime.utcnow().isoformat(),
            suggestions=suggestions
        )
        
        logger.info(f"Successfully generated targeting for: {product_input.product_name}")
        return response
        
    except Exception as e:
        logger.error(f"Error in generate_targeting: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sample-personas")
async def get_sample_personas():
    """Get sample personas for demo purposes"""
    return {
        "sample_personas": [
            {
                "name": "The Conscious Creative",
                "description": "Urban millennials who blend sustainability with artistic expression"
            },
            {
                "name": "The Mindful Minimalist",
                "description": "Values quality over quantity, seeks authentic experiences"
            },
            {
                "name": "The Eco Adventurer",
                "description": "Active lifestyle enthusiasts who prioritize environmental impact"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)