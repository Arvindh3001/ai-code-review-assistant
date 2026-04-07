import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from src.routers.webhook import router as webhook_router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="AI Code Review Assistant",
    description="Context-aware AI-powered code review for GitHub Pull Requests.",
    version="0.1.0",
)

app.include_router(webhook_router)


@app.get("/health")
async def health_check():
    return {"status": "active", "version": "0.1.0"}
