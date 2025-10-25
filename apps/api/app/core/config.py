import os

API_PORT = int(os.getenv("API_PORT", "8000"))

# Database configuration (minimal)
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_PORT = os.getenv("PG_PORT", os.getenv("PG_EXPOSE_PORT", "5432"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    if PG_USER and PG_PASSWORD and PG_DB:
        DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    else:
        # fallback to local sqlite for development
        DATABASE_URL = "sqlite:///./app.db"


