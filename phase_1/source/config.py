
from pathlib import Path
import os

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

# Locate the root .env file relative to this module.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

# Load local configuration for development.
load_dotenv(ENV_PATH, override=True)


def get_required_setting(name: str) -> str:
    # First, try the local environment variable.
    value = os.getenv(name)

    # If unavailable, try Streamlit Cloud Secrets.
    if not value:
        try:
            value = st.secrets[name]
        except Exception:
            value = None

    # Fail clearly if the setting is missing from both places.
    if not value:
        raise RuntimeError(
            f"Missing configuration: {name}. "
            "Check your local .env file or Streamlit Cloud Secrets."
        )

    return str(value)


# Centralized LLM configuration.
GROQ_API_KEY = get_required_setting("GROQ_API_KEY")

# Supabase PostgreSQL connection URL.
DATABASE_URL = get_required_setting("DATABASE_URL")

# Normalize the SQLAlchemy driver.
url = make_url(DATABASE_URL)

if url.drivername == "postgresql":
    url = url.set(drivername="postgresql+psycopg")

DATABASE_URL = url.render_as_string(hide_password=False)
