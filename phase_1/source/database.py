
from sqlalchemy import URL, create_engine, text
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


# Build the connection URL safely, including passwords with special characters.
connection_url = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# Reuse a connection pool rather than creating a new engine for each request.
engine = create_engine(
    connection_url,
    pool_pre_ping=True,  # Detect stale connections before using them.
    pool_size=5,         # Keep a small pool for this application.
    max_overflow=5,      # Allow temporary additional connections under load.
    pool_timeout=10,     # Avoid waiting indefinitely for a connection.
    pool_recycle=1800,   # Periodically recycle long-lived connections.
)


def check_database_connection() -> bool:
    """Verify that PostgreSQL is reachable."""
    with engine.connect() as connection:
        # A lightweight query confirms the connection is usable.
        connection.execute(text("SELECT 1"))

    return True
