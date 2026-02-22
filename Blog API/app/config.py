from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Configuration class"""
    database_url: str = Field(
        default="postgresql://user:1234@localhost:5433/postgres",
        alias="DATABASE_URL"
    )

settings = Settings()