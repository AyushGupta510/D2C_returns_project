from pathlib import Path
import os
from dotenv import load_dotenv

# Locate .env relative to this file, not the notebook's working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)

def get_required_setting(name: str) -> str:
    # Fail clearly if a required credential is missing.
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. Check your .env file."
        )
    return value


# Centralize database and LLM configuration for the entire application.
GROQ_API_KEY = get_required_setting("GROQ_API_KEY")

DB_USER = get_required_setting("DB_USER")
DB_PASSWORD = get_required_setting("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "d2c_returns_db")
