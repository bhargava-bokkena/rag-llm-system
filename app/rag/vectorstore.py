import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings


def get_chroma_client():
    return chromadb.PersistentClient(
        path=settings.VECTOR_DB_DIR,
        settings=ChromaSettings(anonymized_telemetry=False),
    )


def get_collection(name: str = "documents"):
    client = get_chroma_client()
    return client.get_or_create_collection(name=name)

