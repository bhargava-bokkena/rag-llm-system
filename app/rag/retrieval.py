from typing import Any, Dict, List
from app.rag.vectorstore import get_collection
from app.rag.llm import embed_texts


def retrieve(query: str, k: int = 4) -> List[Dict[str, Any]]:
    collection = get_collection("documents")
    q_emb = embed_texts([query])[0]

    res = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    out = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({"text": doc, "metadata": meta, "distance": dist})
    return out


def build_prompt(question: str, contexts: List[Dict[str, Any]]) -> str:
    ctx_block = "\n\n".join(
        [f"[source={c['metadata'].get('source','unknown')}]\n{c['text']}" for c in contexts]
    )
    return f"""Answer the question using ONLY the context. If you cannot, say "I don't know".

Question:
{question}

Context:
{ctx_block}
"""

