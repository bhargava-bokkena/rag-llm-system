from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Load from .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "RAG / LLM System"
    VECTOR_DB_DIR: str = "vectorstore/chroma"

    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4.1-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Ingestion controls
    RESET_COLLECTION: bool = False
    COLLECTION_NAME: str = "documents"


settings = Settings()