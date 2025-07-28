from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.configuration.config import settings
from utils.logger import configure_logging
from api import routes, health

# Setup logging
configure_logging()

# FastAPI instance
app = FastAPI(
    title="TasteTarget API - Qloo + OpenAI",
    description="AI-Powered Cultural Targeting",
    version="3.0.0",
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(routes.router, prefix="/api")
app.include_router(health.router)

# Uvicorn run
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
