from dotenv import load_dotenv
from pathlib import Path

# Automatically find .env in project root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env")

class Config:
    API_URL = "http://localhost:8000"
    BRAND_NAME = "TasteTarget"
    VERSION = "1.0.0"