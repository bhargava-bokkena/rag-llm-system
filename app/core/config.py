from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RAG / LLM System"
    VECTOR_DB_DIR: str = "vectorstore/chroma"

    # We'll use these later for embeddings + LLM calls
    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4.1-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    class Config:
        env_file = ".env"


settings = Settings()

