from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    openai_api_key: str = ""        # optional — only needed for OpenAI embeddings
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-5"
    embedding_model: str = "text-embedding-3-small"

    postgres_dsn: str = "postgresql+asyncpg://gauser:gapassword@localhost:5432/gadb"

    chroma_host: str = "localhost"
    chroma_port: int = 8001

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    courses_dir: str = "./courses"


settings = Settings()
