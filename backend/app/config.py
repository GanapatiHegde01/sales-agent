import os
from dotenv import load_dotenv

# Load .env from project root if present
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/ai_sales_agent"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini / LLM
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Simple API key for protecting chat in dev
    AUTH_API_KEY = os.getenv("AUTH_API_KEY", "dev-api-key")