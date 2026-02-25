from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Document:
    doc_id: str
    text: str
    metadata: Dict[str, Any]


def load_txt_documents(dir_path: str = "data/raw") -> List[Document]:
    base = Path(dir_path)
    docs: List[Document] = []

    for p in base.rglob("*.txt"):
        text = p.read_text(encoding="utf-8")
        docs.append(
            Document(
                doc_id=str(p.relative_to(base)),
                text=text,
                metadata={"source": str(p)},
            )
        )

    return docs


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 80) -> List[str]:
    """
    Simple character-based chunking (dependency-free).
    We'll upgrade to token-based later.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be < chunk_size")

    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap
        if start < 0:
            start = 0
        if end == n:
            break

    return chunks


def make_chunks(docs: List[Document]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    for d in docs:
        chunks = chunk_text(d.text)
        for i, ch in enumerate(chunks):
            records.append(
                {
                    "id": f"{d.doc_id}::chunk{i}",
                    "text": ch,
                    "metadata": {**d.metadata, "doc_id": d.doc_id, "chunk_index": i},
                }
            )

    return records

