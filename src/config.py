import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GITHUB_APP_TOKEN: str = os.getenv("GITHUB_APP_TOKEN", "")
GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
GROQ_MODEL: str = "llama-3.3-70b-versatile"
