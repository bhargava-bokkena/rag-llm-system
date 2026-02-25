from app.core.config import settings
from app.rag.ingestion import load_txt_documents, make_chunks
from app.rag.llm import embed_texts
from app.rag.vectorstore import get_collection


if __name__ == "__main__":
    docs = load_txt_documents("data/raw")
    print(f"Loaded {len(docs)} documents")

    records = make_chunks(docs)
    print(f"Created {len(records)} chunks")

    texts = [r["text"] for r in records]
    ids = [r["id"] for r in records]
    metas = [r["metadata"] for r in records]

    embeddings = embed_texts(texts)

    # ✅ dimension/model guard goes BEFORE writing to Chroma
    dim = len(embeddings[0])
    for m in metas:
        m["embedding_model"] = settings.EMBEDDING_MODEL
        m["embedding_dim"] = dim

    collection = get_collection("documents")

    # simple dev reset: delete ids if they exist
    try:
        collection.delete(ids=ids)
    except Exception:
        pass

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metas,
        embeddings=embeddings,
    )

    print(f"Stored {len(records)} chunks WITH explicit embeddings in Chroma.")
    print(f"Embedding model: {settings.EMBEDDING_MODEL} | dim={dim}")
