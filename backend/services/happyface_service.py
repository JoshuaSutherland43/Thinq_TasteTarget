from core.configuration.config import settings
from PIL import Image

import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/api/test-visual-generation")
async def test_visual_generation():
    """Test visual generation capability"""
    try:
        # Test if Hugging Face Space is accessible
        try:
            client = Client("Samkelo28/taste-target-visual-generator")
            status = "connected"
            message = "Hugging Face Space is accessible"
        except Exception as e:
            status = "fallback"
            message = f"Using local generation (HF Space error: {str(e)})"

        # Test local generation
        img = Image.new("RGB", (100, 100), color="red")
        local_status = "available"

        return {
            "huggingface_space": {
                "status": status,
                "message": message,
                "space_url": "https://huggingface.co/spaces/Samkelo28/taste-target-visual-generator",
            },
            "local_generation": {
                "status": local_status,
                "message": "Local generation available as fallback",
            },
            "recommendation": "Visual generation is ready to use",
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


@router.post("/api/generate-visual")
async def generate_visual(request: VisualGenerationRequest):
    """Generate marketing visual using Hugging Face Space"""
    try:
        logger.info(f"Generating visual for persona: {request.persona_name}")

        # Try to use the Hugging Face Space first
        try:
            # Initialize Gradio client for your Space
            logger.info(f"Attempting to use Hugging Face Space for visual generation")

            client = Client("Samkelo28/taste-target-visual-generator")

            # Call the Space with your parameters
            result = await asyncio.to_thread(
                client.predict,
                request.persona_name,
                request.brand_values,
                request.product_description,
                request.style_preference,
                request.image_type,
                api_name="/predict",
            )

            # The result should be a file path to the generated image
            if result and isinstance(result, str) and os.path.exists(result):
                # Read the image file and convert to base64
                with open(result, "rb") as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode("utf-8")

                # Clean up the temporary file
                try:
                    os.remove(result)
                except:
                    pass

                logger.info(f"Successfully generated visual for {request.persona_name}")

                return {
                    "status": "success",
                    "image_data": f"data:image/png;base64,{img_base64}",
                    "message": "Visual generated successfully with AI",
                }
            else:
                raise Exception("Invalid result from Hugging Face Space")

        except Exception as hf_error:
            logger.warning(f"Hugging Face Space error: {str(hf_error)}")
            logger.info("Falling back to local generation")

            # Fallback: Generate a stylized placeholder image locally
            from PIL import Image, ImageDraw, ImageFont
            import io
            import math

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
