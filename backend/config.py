from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    project_id: str = "skillbridge-rwanda"
    location: str = "us-central1"

    gemini_model: str = "gemini-1.5-flash-002"
    embedding_model: str = "text-embedding-004"

    vector_search_index_endpoint: str = ""
    vector_search_index_id: str = ""
    vector_search_deployed_index_id: str = ""

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/skillbridge"

    firestore_collection: str = "chat_sessions"

    cors_origins: list[str] = ["http://localhost:3000", "https://skillbridge-rwanda.web.app"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
