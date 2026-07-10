"""
Configuration module for Study Assistant Bot.
Loads and manages all environment variables and settings.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Base paths
BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
GENERATED_DIR = STORAGE_DIR / "generated"
LOGS_DIR = BASE_DIR / "logs"


class Config:
    """Base configuration class."""

    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_BOT_USERNAME: str = os.getenv("TELEGRAM_BOT_USERNAME", "study_bot")
    
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required. Please set it in .env")

    # AI Provider
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai").lower()
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required when using OpenAI")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./study_bot.db")
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "sqlite")

    # Storage
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")
    STORAGE_LOCAL_PATH: str = os.getenv("STORAGE_LOCAL_PATH", str(UPLOADS_DIR))
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME", "study-bot")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # RAG Settings
    RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "true").lower() == "true"
    EMBEDDINGS_MODEL: str = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", str(STORAGE_DIR / "faiss_db"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", str(LOGS_DIR / "bot.log"))

    # Server
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    POLLING_INTERVAL: int = int(os.getenv("POLLING_INTERVAL", "1"))

    # Feature Flags
    ENABLE_REMINDERS: bool = os.getenv("ENABLE_REMINDERS", "true").lower() == "true"
    ENABLE_QUIZ: bool = os.getenv("ENABLE_QUIZ", "true").lower() == "true"
    ENABLE_FLASHCARDS: bool = os.getenv("ENABLE_FLASHCARDS", "true").lower() == "true"
    ENABLE_TRANSLATOR: bool = os.getenv("ENABLE_TRANSLATOR", "true").lower() == "true"
    ENABLE_PLANNER: bool = os.getenv("ENABLE_PLANNER", "true").lower() == "true"
    ENABLE_RAG: bool = os.getenv("ENABLE_RAG", "true").lower() == "true"

    # Admin Settings
    _admin_ids_str: str = os.getenv("ADMIN_USER_IDS", "")
    ADMIN_USER_IDS: List[int] = [
        int(uid.strip()) for uid in _admin_ids_str.split(",") if uid.strip()
    ] if _admin_ids_str else []

    # Pagination and defaults
    FLASHCARDS_PER_PAGE: int = 1
    QUIZ_QUESTIONS_DEFAULT: int = 5
    MAX_CONTEXT_LENGTH: int = 4000

    # Timeouts
    OPENAI_TIMEOUT: int = 30
    OPENAI_MAX_TOKENS: int = 2000

    # File handling
    SUPPORTED_DOCUMENTS: tuple = (".pdf", ".docx", ".txt")
    MAX_FILE_SIZE_BYTES: int = MAX_UPLOAD_SIZE_MB * 1024 * 1024

    # Supported languages for translation
    SUPPORTED_LANGUAGES: dict = {
        "en": "English",
        "fr": "French",
        "es": "Spanish",
        "ar": "Arabic",
        "am": "Amharic",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ja": "Japanese",
        "zh": "Chinese",
    }

    # Quiz difficulty levels
    QUIZ_DIFFICULTY_LEVELS: list = ["easy", "medium", "hard"]

    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if user is admin."""
        return user_id in cls.ADMIN_USER_IDS


# Create necessary directories
for directory in [UPLOADS_DIR, GENERATED_DIR, LOGS_DIR, Path(Config.VECTOR_DB_PATH)]:
    directory.mkdir(parents=True, exist_ok=True)


def get_config() -> Config:
    """Get application configuration."""
    return Config
