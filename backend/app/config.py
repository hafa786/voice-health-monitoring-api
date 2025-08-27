from pydantic import BaseModel # type: ignore
import os


class Settings(BaseModel):
    api_key: str = os.getenv("API_KEY", "change-me")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*") # comma-separated
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", 25))


settings = Settings()