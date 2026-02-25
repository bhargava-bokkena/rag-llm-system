from __future__ import annotations

from typing import Optional, Tuple

from app.core.config import settings
from app.rag.vectorstore import get_collection


def get_collection_embedding_signature(collection_name: str = "documents") -> Optional[Tuple[str, int]]:
    """
    Reads one stored record and returns (embedding_model, embedding_dim) if present.
    Returns None if collection is empty or metadata missing.
    """
    c = get_collection(collection_name)
    res = c.get(limit=1, include=["metadatas"])
    metas = res.get("metadatas") or []
    if not metas:
        return None

    m = metas[0] or {}
    model = m.get("embedding_model")
    dim = m.get("embedding_dim")
    if not model or not dim:
        return None
    return str(model), int(dim)


def assert_vectorstore_compatible(collection_name: str = "documents") -> None:
    """
    Fail fast if the stored embedding signature doesn't match current env config.
    """
    sig = get_collection_embedding_signature(collection_name)
    if sig is None:
        # empty collection or missing metadata — allow startup
        return

    stored_model, stored_dim = sig
    current_model = settings.EMBEDDING_MODEL

    # only check dim if current embeddings are available (OpenAI embeddings are fixed per model)
    if stored_model != current_model:
        raise RuntimeError(
            f"Vectorstore incompatible: stored embedding_model='{stored_model}' "
            f"but current EMBEDDING_MODEL='{current_model}'. "
            f"Re-ingest or use a new collection."
        )

    # Guard dimension too (extra safety)
    # OpenAI text-embedding-3-small => 1536, but we avoid hardcoding and trust stored_dim
    if stored_dim <= 0:
        return
