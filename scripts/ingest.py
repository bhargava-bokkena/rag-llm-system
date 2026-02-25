from app.core.config import settings
from app.rag.ingestion import load_txt_documents, make_chunks
from app.rag.llm import embed_texts
from app.rag.vectorstore import get_collection, get_chroma_client


if __name__ == "__main__":
    docs = load_txt_documents("data/raw")
    print(f"Loaded {len(docs)} documents")

    records = make_chunks(docs)
    print(f"Created {len(records)} chunks")

    texts = [r["text"] for r in records]
    ids = [r["id"] for r in records]
    metas = [r["metadata"] for r in records]

    embeddings = embed_texts(texts)

    dim = len(embeddings[0])
    for m in metas:
        m["embedding_model"] = settings.EMBEDDING_MODEL
        m["embedding_dim"] = dim

    collection_name = settings.COLLECTION_NAME

    if settings.RESET_COLLECTION:
        print(f"RESET_COLLECTION=true -> deleting and recreating '{collection_name}'")
        client = get_chroma_client()
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    collection = get_collection(collection_name)

    # safe "upsert": delete only ids we are writing
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
    print(f"Collection: {collection_name} | Embedding model: {settings.EMBEDDING_MODEL} | dim={dim}")