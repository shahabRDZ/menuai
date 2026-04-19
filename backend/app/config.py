from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://menuai:menuai_dev@localhost:5432/menuai"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "dev-secret-change-in-prod"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"

    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def async_database_url(self) -> str:
        """Force the async driver. Railway/Heroku/Render expose URLs as
        ``postgres://`` or ``postgresql://``; SQLAlchemy's async engine
        expects ``postgresql+asyncpg://``.
        """
        url = self.database_url
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://") :]
        if url.startswith("postgresql://") and "+asyncpg" not in url:
            url = "postgresql+asyncpg://" + url[len("postgresql://") :]
        return url


settings = Settings()
