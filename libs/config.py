# libs/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # ===== Database Settings =====
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ===== Redis / Celery =====
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str

    # ===== S3 / MinIO =====
    S3_ENDPOINT: str = Field(..., description="MinIO or S3 endpoint URL e.g. http://minio:9000")
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str = "us-east-1"
    S3_BUCKET_MODELS: str = "models"
    S3_BUCKET_ADAPTERS: str = "adapters"

    # ===== Queues for Runners =====
    QUEUE_PT: str = "pt"
    QUEUE_ONNX: str = "onnx"

    class Config:
        env_file = ".env"  # or "configs/.env.dev" in local development
        env_file_encoding = "utf-8"


settings = Settings()
