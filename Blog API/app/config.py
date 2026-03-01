from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, field_validator

class Settings(BaseSettings):
    """Configuration class"""
    database_url: str = Field(
        default="postgresql://postgres:1234@localhost:5432/blog_api",
        alias="DATABASE_URL",
        description="PostgreSQL connection string"
    )

    jwt_secret: SecretStr = Field(
        alias='JWT_SECRET',
        description="Secret key for JWT token signing (min 32 chars)",
        min_length=32
    )

    jwt_algorithm: str = Field(
        default="HS256",
        alias='JWT_ALGORITHMN',
        description="JWT signing algorithm",
        pattern='^(HS256|RS256|HS512)$'
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        validate_default=True
    )

settings = Settings()