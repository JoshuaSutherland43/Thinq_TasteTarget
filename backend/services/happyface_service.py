# External packages
from fastapi import APIRouter, UploadFile, File, Form

from PIL import Image, ImageDraw, ImageFont
import io
import math
from httpx import Client  # or use httpx.AsyncClient if neede
from gradio_client import Client

# Built-in modules
import asyncio
import os
import base64
import logging
import io

# Local or project imports
from core.configuration.config import settings
from models.schemas import VisualGenerationRequest
from fastapi.responses import JSONResponse
import shutil
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/api/generate-visual")
async def generate_visual(request: VisualGenerationRequest):
    """Generate marketing visual using Hugging Face Space"""
    # [Your existing code remains exactly the same]
    try:
        logger.info(f"Generating visual for persona: {request.persona_name}")

        # Try to use the Hugging Face Space first
        try:
            # Initialize Gradio client for your Space
            logger.info(f"Attempting to use Hugging Face Space for visual generation")

            client = Client("Samkelo28/taste-target-visual-generator")

            try:
                result = await asyncio.to_thread(
                    client.predict,
                    request.persona_name,
                    request.brand_values,
                    request.product_description,
                    request.style_preference,
                    request.image_type,
                    api_name="/predict",
                )
            except Exception as e:
                raise RuntimeError(f"Hugging Face predict() failed: {e}")

            # Validate result
            if not result:
                raise ValueError("No response from Hugging Face Space.")

            if isinstance(result, str):
                if os.path.exists(result):
                    with open(result, "rb") as img_file:
                        img_data = img_file.read()
                        img_base64 = base64.b64encode(img_data).decode("utf-8")
                    try:
                        os.remove(result)
                    except:
                        pass
                    logger.info(
                        f"Successfully generated visual for {request.persona_name}"
                    )
                    return {
                        "status": "success",
                        "image_data": f"data:image/png;base64,{img_base64}",
                        "message": "Visual generated successfully with AI",
                    }
                else:
                    raise FileNotFoundError(
                        f"File not found at predicted path: {result}"
                    )
            else:
                raise TypeError(
                    f"Unexpected result type from Hugging Face Space: {type(result)}"
                )

        except Exception as hf_error:
            logger.warning(f"Hugging Face Space error: {str(hf_error)}")
            logger.info("Falling back to local generation")

            # Create a high-quality placeholder based on style
            width, height = 512, 512

            # Style-specific colors and designs
            style_configs = {
                "minimalist clean": {
                    "bg_color": (250, 250, 250),
                    "accent_color": (0, 0, 0),
                    "text_color": (0, 0, 0),
                    "font_size": 24,
                },
                "bold vibrant": {
                    "bg_color": (255, 0, 128),
                    "accent_color": (0, 255, 255),
                    "text_color": (255, 255, 255),
                    "font_size": 32,
                },
                "luxury premium": {
                    "bg_color": (20, 20, 20),
                    "accent_color": (218, 165, 32),
                    "text_color": (218, 165, 32),
                    "font_size": 28,
                },
                "natural organic": {
                    "bg_color": (245, 245, 220),
                    "accent_color": (34, 139, 34),
                    "text_color": (34, 139, 34),
                    "font_size": 26,
                },
                "tech futuristic": {
                    "bg_color": (10, 10, 50),
                    "accent_color": (0, 255, 255),
                    "text_color": (0, 255, 255),
                    "font_size": 30,
                },
                "artistic creative": {
                    "bg_color": (255, 245, 238),
                    "accent_color": (255, 69, 0),
                    "text_color": (139, 69, 19),
                    "font_size": 28,
                },
            }

            config = style_configs.get(
                request.style_preference, style_configs["minimalist clean"]
            )

            # Create image with anti-aliasing
            img = Image.new("RGBA", (width, height), (*config["bg_color"], 255))
            draw = ImageDraw.Draw(img)

            # Generate logo design based on type
            if request.image_type == "logo":
                # Extract brand initials
                brand_name = request.product_description.strip()
                initials = "".join([word[0].upper() for word in brand_name.split()[:2]])
                if not initials:
                    initials = brand_name[:2].upper()

                # Create logo based on style
                if request.style_preference == "minimalist clean":
                    # Circular logo with initials
                    draw.ellipse(
                        [156, 156, 356, 356], outline=config["accent_color"], width=4
                    )
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
                        )
                    except:
                        font = ImageFont.load_default()
                    bbox = draw.textbbox((0, 0), initials, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    draw.text(
                        (256 - text_width // 2, 256 - text_height // 2),
                        initials,
                        fill=config["accent_color"],
                        font=font,
                    )

                elif request.style_preference == "bold vibrant":
                    # Gradient-style square logo
                    for i in range(100):
                        alpha = int(255 * (1 - i / 100))
                        color = (*config["accent_color"], alpha)
                        draw.rectangle(
                            [156 + i, 156 + i, 356 - i, 356 - i], outline=color, width=2
                        )
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60
                        )
                    except:
                        font = ImageFont.load_default()
                    draw.text(
                        (256, 256),
                        initials,
                        fill=config["text_color"],
                        font=font,
                        anchor="mm",
                    )

                elif request.style_preference == "luxury premium":
                    # Diamond shape with gold accent
                    points = [(256, 106), (406, 256), (256, 406), (106, 256)]
                    draw.polygon(points, outline=config["accent_color"], width=3)
                    # Inner diamond
                    inner_points = [(256, 156), (356, 256), (256, 356), (156, 256)]
                    draw.polygon(inner_points, outline=config["accent_color"], width=2)
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 42
                        )
                    except:
                        font = ImageFont.load_default()
                    draw.text(
                        (256, 256),
                        initials,
                        fill=config["accent_color"],
                        font=font,
                        anchor="mm",
                    )

                elif request.style_preference == "natural organic":
                    # Leaf-inspired logo
                    # Draw leaf shapes
                    for angle in range(0, 360, 45):
                        x = 256 + 80 * (angle % 90) / 90
                        y = 256 - 80 * (angle % 90) / 90
                        draw.arc(
                            [x - 40, y - 40, x + 40, y + 40],
                            angle,
                            angle + 90,
                            fill=config["accent_color"],
                            width=3,
                        )
                    # Center circle
                    draw.ellipse(
                        [226, 226, 286, 286],
                        fill=config["bg_color"],
                        outline=config["accent_color"],
                        width=3,
                    )
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36
                        )
                    except:
                        font = ImageFont.load_default()
                    draw.text(
                        (256, 256),
                        initials,
                        fill=config["accent_color"],
                        font=font,
                        anchor="mm",
                    )

                elif request.style_preference == "tech futuristic":
                    # Hexagon tech logo
                    hex_points = []
                    for i in range(6):
                        angle = i * 60 * math.pi / 180
                        x = 256 + 100 * math.cos(angle)
                        y = 256 + 100 * math.sin(angle)
                        hex_points.append((x, y))
                    draw.polygon(hex_points, outline=config["accent_color"], width=3)
                    # Inner hex
                    inner_hex = []
                    for i in range(6):
                        angle = i * 60 * math.pi / 180
                        x = 256 + 60 * math.cos(angle)
                        y = 256 + 60 * math.sin(angle)
                        inner_hex.append((x, y))
                    draw.polygon(inner_hex, outline=config["accent_color"], width=2)
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
                        )
                    except:
                        font = ImageFont.load_default()
                    draw.text(
                        (256, 256),
                        initials,
                        fill=config["accent_color"],
                        font=font,
                        anchor="mm",
                    )

                else:  # artistic creative
                    # Abstract artistic logo
                    import random

                    random.seed(hash(brand_name))
                    for _ in range(8):
                        x1 = random.randint(156, 256)
                        y1 = random.randint(156, 256)
                        x2 = random.randint(256, 356)
                        y2 = random.randint(256, 356)
                        draw.arc(
                            [x1, y1, x2, y2],
                            0,
                            180,
                            fill=config["accent_color"],
                            width=3,
                        )
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54
                        )
                    except:
                        font = ImageFont.load_default()
                    draw.text(
                        (256, 256),
                        initials,
                        fill=config["accent_color"],
                        font=font,
                        anchor="mm",
                    )

                # Add brand name below logo
                try:
                    small_font = ImageFont.truetype(
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
                    )
                except:
                    small_font = ImageFont.load_default()

                draw.text(
                    (256, 420),
                    brand_name,
                    fill=config["text_color"],
                    font=small_font,
                    anchor="mt",
                )

            else:
                # Marketing visual generation (existing code)
                if request.style_preference == "minimalist clean":
                    draw.ellipse(
                        [156, 156, 356, 356], outline=config["accent_color"], width=3
                    )
                elif request.style_preference == "bold vibrant":
                    draw.rectangle([100, 100, 300, 300], fill=config["accent_color"])
                    draw.ellipse([212, 212, 412, 412], fill=config["bg_color"])
                elif request.style_preference == "luxury premium":
                    draw.rectangle([106, 206, 406, 306], fill=config["accent_color"])
                elif request.style_preference == "natural organic":
                    for i in range(5):
                        x = 256 + i * 30 - 60
                        y = 256 + i * 20 - 40
                        draw.ellipse(
                            [x - 50, y - 20, x + 50, y + 20],
                            fill=config["accent_color"],
                        )
                elif request.style_preference == "tech futuristic":
                    for i in range(0, width, 50):
                        draw.line(
                            [(i, 0), (i, height)], fill=config["accent_color"], width=1
                        )
                        draw.line(
                            [(0, i), (width, i)], fill=config["accent_color"], width=1
                        )
                else:
                    draw.arc(
                        [100, 100, 400, 400],
                        0,
                        270,
                        fill=config["accent_color"],
                        width=5,
                    )

                # Add text
                try:
                    font = ImageFont.truetype(
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                        config["font_size"],
                    )
                except:
                    font = ImageFont.load_default()

                text = request.persona_name
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                draw.text(
                    (text_x, height - 80), text, fill=config["text_color"], font=font
                )

                product_text = (
                    request.product_description[:30] + "..."
                    if len(request.product_description) > 30
                    else request.product_description
                )
                try:
                    small_font = ImageFont.truetype(
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16
                    )
                except:
                    small_font = ImageFont.load_default()

                bbox = draw.textbbox((0, 0), product_text, font=small_font)
                text_width = bbox[2] - bbox[0]
                text_x = (width - text_width) // 2
                draw.text(
                    (text_x, height - 50),
                    product_text,
                    fill=config["text_color"],
                    font=small_font,
                )

            # Add TasteTarget watermark for marketing visuals only
            if request.image_type != "logo":
                watermark = "TasteTarget AI"
                bbox = draw.textbbox((0, 0), watermark, font=small_font)
                draw.text(
                    (10, height - 20),
                    watermark,
                    fill=config["text_color"],
                    font=small_font,
                )

            # Convert to base64
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG", quality=95)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")

            message = (
                "Logo generated successfully"
                if request.image_type == "logo"
                else "Visual generated successfully"
            )

            return {
                "status": "success",
                "image_data": f"data:image/png;base64,{img_base64}",
                "message": f"{message} (local generation)",
            }

    except Exception as e:
        logger.error(f"Visual generation error: {str(e)}")
        return {"status": "error", "message": f"Failed to generate visual: {str(e)}"}


# ADD THIS NEW ENDPOINT AFTER THE EXISTING generate_visual ENDPOINT
@router.post("/api/generate-cultural-visual")
async def generate_cultural_visual(request: dict):
    """Generate visuals that incorporate cultural insights from Qloo data"""
    try:
        persona_data = request.get("persona_data", {})
        product_info = request.get("product_info", {})
        visual_type = request.get("visual_type", "poster")
        style_preference = request.get("style_preference", "minimalist clean")
        custom_elements = request.get("custom_elements", "")

        # Extract cultural interests
        cultural_interests = persona_data.get("cultural_interests", {})
        psychographics = persona_data.get("psychographics", [])
        persona_name = persona_data.get("name", "Target Customer")

        # Build a culturally-informed description
        cultural_description = f"{product_info.get('name', 'product')}"

        # Add cultural elements to the description for better AI generation
        cultural_context = []

        if custom_elements:
            cultural_description += f" - {custom_elements}"
        else:
            # Add cultural context based on interests
            if cultural_interests.get("music"):
                music_styles = ", ".join(cultural_interests["music"][:2])
                cultural_context.append(f"inspired by {music_styles} vibes")

            if cultural_interests.get("fashion"):
                fashion_style = (
                    cultural_interests["fashion"][0]
                    if cultural_interests["fashion"]
                    else ""
                )
                if fashion_style:
                    cultural_context.append(f"{fashion_style} aesthetic")

            if cultural_interests.get("dining"):
                dining_pref = (
                    cultural_interests["dining"][0]
                    if cultural_interests["dining"]
                    else ""
                )
                if dining_pref:
                    cultural_context.append(f"appeals to {dining_pref} enthusiasts")

            if psychographics:
                cultural_context.append(f"designed for {psychographics[0]} mindset")

        # Combine cultural context into description
        if cultural_context:
            cultural_description += " - " + ", ".join(cultural_context)

        logger.info(
            f"Generating culturally-informed visual for persona: {persona_name}"
        )
        logger.info(f"Cultural elements being incorporated: {cultural_interests}")
        logger.info(f"Enhanced description: {cultural_description}")

        # Determine image type
        image_type = (
            "logo" if visual_type == "logo" and not custom_elements else "marketing"
        )

        # Create a visual request with cultural enhancements
        visual_request = VisualGenerationRequest(
            persona_name=persona_name,
            brand_values=product_info.get("brand_values", "quality, innovation"),
            product_description=cultural_description,
            style_preference=style_preference,
            image_type=image_type,
        )

        # Use the existing generate_visual function with enhanced description
        result = await generate_visual(visual_request)

        # Add cultural metadata to the result
        if result.get("status") == "success":
            result["cultural_elements"] = cultural_interests
            result["psychographics"] = psychographics
            result["generation_type"] = "cultural_enhanced"
            result["prompt_summary"] = (
                f"Created for {persona_name} with {len(psychographics)} key traits and {len(cultural_context)} cultural elements"
            )

            # Log successful cultural generation
            logger.info(
                f"Successfully generated cultural visual for {persona_name} with {len(cultural_context)} cultural elements"
            )

        return result

    except Exception as e:
        logger.error(f"Cultural visual generation error: {str(e)}")
        import traceback

        logger.error(traceback.format_exc())

        # Fallback to standard generation if cultural generation fails
        try:
            logger.info("Attempting fallback to standard visual generation")

            # Create a basic visual request
            basic_request = VisualGenerationRequest(
                persona_name=request.get("persona_data", {}).get("name", "Customer"),
                brand_values=request.get("product_info", {}).get(
                    "brand_values", "quality"
                ),
                product_description=request.get("product_info", {}).get(
                    "name", "Product"
                ),
                style_preference=request.get("style_preference", "minimalist clean"),
                image_type=(
                    "logo" if request.get("visual_type") == "logo" else "marketing"
                ),
            )

            result = await generate_visual(basic_request)
            result["generation_type"] = "fallback"
            return result

        except Exception as fallback_error:
            logger.error(f"Fallback generation also failed: {str(fallback_error)}")
            return {
                "status": "error",
                "message": f"Failed to generate visual: {str(e)}",
            }
