import asyncio
import json
from openai import OpenAI
from fastapi import HTTPException
from core.configuration.config import settings
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

QLOO_API_KEY = settings.QLOO_API_KEY
QLOO_API_URL = settings.QLOO_API_URL

# Qloo API Integration (same as before)
async def call_qloo_api(product_info: dict) -> List[dict]:
    """Call Qloo API v2 for taste-based insights"""
    if not QLOO_API_KEY:
        logger.warning("QLOO_API_KEY not found, using mock data")
        return await mock_qloo_api(product_info)
    
    headers = {
        "X-Api-Key": QLOO_API_KEY,
        "Content-Type": "application/json"
    }
    
    clusters = []
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            tag_mappings = {
                "sustainability": ["urn:tag:genre:lifestyle:eco-friendly", "urn:tag:genre:lifestyle:sustainable"],
                "innovation": ["urn:tag:genre:tech:innovative", "urn:tag:genre:lifestyle:modern"],
                "luxury": ["urn:tag:genre:lifestyle:luxury", "urn:tag:genre:lifestyle:premium"],
                "minimalism": ["urn:tag:genre:lifestyle:minimalist", "urn:tag:genre:lifestyle:simple"],
                "ethical": ["urn:tag:genre:lifestyle:ethical", "urn:tag:genre:lifestyle:conscious"],
                "quality": ["urn:tag:genre:lifestyle:quality", "urn:tag:genre:lifestyle:premium"]
            }
            
            # Query Qloo for insights based on brand values
            for i, value in enumerate(product_info.get('brand_values', [])[:3]):
                try:
                    tags = tag_mappings.get(value, [f"urn:tag:genre:lifestyle:{value}"])
                    
                    base_url = f"{QLOO_API_URL}/v2/insights"
                    params = {
                        "filter.type": "urn:demographics",
                        "signal.interests.tags": tags[0] if tags else f"urn:tag:genre:lifestyle:{value}"
                    }
                    
                    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                    url = f"{base_url}?{query_string}"
                    
                    logger.info(f"Calling Qloo API: {url}")
                    response = await client.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        insights = response.json()
                        logger.info(f"Qloo insights received for {value}")
                        
                        cluster = convert_qloo_insights_to_cluster(insights, value, i)
                        if cluster:
                            clusters.append(cluster)
                    else:
                        logger.warning(f"Qloo API returned {response.status_code} for {value}")
                        
                except Exception as e:
                    logger.error(f"Error querying Qloo for {value}: {e}")
                    
    except Exception as e:
        logger.error(f"Qloo API error: {str(e)}")
    
    if clusters:
        logger.info(f"Successfully retrieved {len(clusters)} clusters from Qloo")
        return clusters
    else:
        logger.warning("No usable data from Qloo API, using mock data")
        return await mock_qloo_api(product_info)

def convert_qloo_insights_to_cluster(insights: dict, cluster_name: str, index: int) -> dict:
    """Convert Qloo API v2 insights response to our cluster format"""
    try:
        cluster = {
            "cluster_id": f"qloo_{cluster_name}_{index}",
            "interests": {
                "music": [],
                "reading": [],
                "dining": [],
                "travel": [],
                "fashion": []
            }
        }
        
        # Parse Qloo insights data
        if "data" in insights:
            data = insights["data"]
            
            if isinstance(data, list):
                for item in data[:10]:
                    if "category" in item and "name" in item:
                        category = item["category"].lower()
                        name = item["name"]
                        
                        # Map to our categories
                        if "music" in category or "artist" in category:
                            cluster["interests"]["music"].append(name)
                        elif "book" in category or "author" in category:
                            cluster["interests"]["reading"].append(name)
                        elif "restaurant" in category or "food" in category:
                            cluster["interests"]["dining"].append(name)
                        elif "destination" in category or "travel" in category:
                            cluster["interests"]["travel"].append(name)
                        elif "brand" in category or "fashion" in category:
                            cluster["interests"]["fashion"].append(name)
            
            # Ensure each category has at least some interests
            for category in cluster["interests"]:
                if not cluster["interests"][category]:
                    cluster["interests"][category] = get_default_interests(category, cluster_name)
        
        return cluster
        
    except Exception as e:
        logger.error(f"Error converting Qloo insights: {e}")
        return None

def get_default_interests(category: str, cluster_name: str) -> List[str]:
    """Get default interests for a category based on cluster name"""
    defaults = {
        "music": {
            "sustainability": ["indie folk", "acoustic", "world music"],
            "innovation": ["electronic", "experimental", "synth"],
            "luxury": ["jazz", "classical", "lounge"],
            "default": ["pop", "indie", "alternative"]
        },
        "reading": {
            "sustainability": ["eco blogs", "philosophy", "nature writing"],
            "innovation": ["tech blogs", "sci-fi", "futurism"],
            "luxury": ["art books", "biographies", "luxury magazines"],
            "default": ["bestsellers", "blogs", "magazines"]
        },
        "dining": {
            "sustainability": ["farm-to-table", "vegan", "organic"],
            "innovation": ["molecular gastronomy", "fusion", "pop-ups"],
            "luxury": ["fine dining", "michelin", "wine bars"],
            "default": ["cafes", "local cuisine", "brunch"]
        },
        "travel": {
            "sustainability": ["eco-lodges", "hiking", "nature"],
            "innovation": ["smart cities", "tech hubs", "urban"],
            "luxury": ["resorts", "exclusive destinations", "yachts"],
            "default": ["city breaks", "cultural sites", "weekend trips"]
        },
        "fashion": {
            "sustainability": ["sustainable brands", "vintage", "ethical"],
            "innovation": ["techwear", "smart fashion", "futuristic"],
            "luxury": ["designer", "couture", "bespoke"],
            "default": ["contemporary", "trendy", "seasonal"]
        }
    }
    
    return defaults.get(category, {}).get(cluster_name, defaults[category]["default"])[:5]

async def mock_qloo_api(product_info: dict) -> List[dict]:
    """Fallback mock data when Qloo API is unavailable"""
    await asyncio.sleep(0.5)
    
    clusters = []
    
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

