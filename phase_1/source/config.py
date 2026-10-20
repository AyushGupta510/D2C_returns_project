
from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

# Locate the root .env file relative to this module.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

# Load the project configuration, overriding stale environment values.
load_dotenv(ENV_PATH, override=True)


def get_required_setting(name: str) -> str:
    # Fail early with a clear message if a credential is missing.
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            f"Check {ENV_PATH}"
        )
    return value


# Centralized LLM configuration.
GROQ_API_KEY = get_required_setting("GROQ_API_KEY")

# Use one connection URL for the Supabase PostgreSQL database.
DATABASE_URL = get_required_setting("DATABASE_URL")

# Normalize the SQLAlchemy driver without exposing credentials.
url = make_url(DATABASE_URL)

if url.drivername == "postgresql":
    url = url.set(drivername="postgresql+psycopg")

DATABASE_URL = url.render_as_string(hide_password=False)
