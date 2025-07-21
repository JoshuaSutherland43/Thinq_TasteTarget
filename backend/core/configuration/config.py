from dotenv import load_dotenv
from pathlib import Path
import os

# Automatically find .env in project root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env")

class Config:
    API_URL = "http://localhost:8000"
    BRAND_NAME = "TasteTarget"
    VERSION = "1.0.0"
    

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    QLOO_API_KEY = os.getenv("QLOO_API_KEY")
    QLOO_API_URL = os.getenv("QLOO_API_URL", "https://hackathon.api.qloo.com")
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
