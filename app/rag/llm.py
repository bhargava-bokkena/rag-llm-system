from __future__ import annotations

from typing import List
import httpx

from app.core.config import settings


def _client() -> httpx.Client:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")
    return httpx.Client(
        base_url=settings.OPENAI_BASE_URL,
        headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
        timeout=30.0,
    )


def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []

    payload = {"model": settings.EMBEDDING_MODEL, "input": texts}

    with _client() as client:
        r = client.post("/embeddings", json=payload)
        r.raise_for_status()
        data = r.json()

    return [item["embedding"] for item in data["data"]]


def chat(prompt: str) -> str:
    payload = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You answer using only provided context. If missing, say you don't know."},
            {"role": "user", "content": prompt},
        ],
    }

    with _client() as client:
        r = client.post("/chat/completions", json=payload)
        r.raise_for_status()
        data = r.json()

    return data["choices"][0]["message"]["content"]

