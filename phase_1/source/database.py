
from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Locate the project root and load its .env configuration.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Read the Supabase connection URL without hardcoding credentials.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from the project .env file.")

# Use psycopg 3 and require encrypted communication with Supabase.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,  # Check stale connections before using them.
    pool_size=5,
    max_overflow=5,
    pool_timeout=10,
)

def check_database_connection():
    # Verify that the application can reach the cloud database.
    with engine.connect() as connection:
        return connection.execute(
            text("SELECT current_database()")
        ).scalar_one()
