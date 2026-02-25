Production-Style RAG / LLM System

This project implements a complete production-style RAG (Retrieval-Augmented Generation) workflow, taking a document set from:

**Ingestion → Chunking → Embeddings → Vector DB (Chroma) → Retrieval → LLM Answering → API Serving → Logging/Tracing → Evaluation → Docker → CI**

It is designed to imitate how modern enterprise LLM/RAG systems are built.

---

## Features

This project includes:

- Document ingestion and deterministic chunking (`data/raw/`)
- OpenAI embeddings (`text-embedding-3-small`, 1536-dim)
- Chroma vector database with persistent storage
- Retrieval pipeline (top-K) with sources and similarity distances
- LLM answer synthesis grounded strictly in retrieved context
- Request tracing and latency metrics (`x-trace-id`, `x-duration-ms`)
- Evaluation harness (`scripts/eval.py`)
- Dockerized API service with persistent vectorstore volume mount
- Pytest smoke tests
- GitHub Actions CI (pytest + Docker build)
- Safety guard: embedding metadata + startup compatibility check
- Operational controls: `RESET_COLLECTION` and `COLLECTION_NAME`

---

## How to Run Locally

### Create virtual environment and install dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Create .env
cp .env.example .env

Set at minimum:

OPENAI_API_KEY=YOUR_KEY_HERE

Recommended defaults:

OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_DB_DIR=vectorstore/chroma
COLLECTION_NAME=documents
RESET_COLLECTION=false
Ingest Documents

Put .txt files into data/raw/, then run:

python -m scripts.ingest
Run the API
uvicorn app.main:app --reload --port 8000

Health check:

curl http://127.0.0.1:8000/api/v1/health

Ask a question:

curl -X POST "http://127.0.0.1:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the internal knowledge base contain?","top_k":2}'
Evaluation

With the API running:

python -m scripts.eval
Run with Docker
Build image
docker build -t rag-llm-system:latest .
Run container
docker run --rm -p 8000:8000 --env-file .env rag-llm-system:latest
Run with persistent vector store
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  -v "$(pwd)/vectorstore/chroma:/app/vectorstore/chroma" \
  rag-llm-system:latest
High-Level Architecture Diagram
data/raw/*.txt
        |
        v
+----------------------+
| Ingestion Job         |
| scripts/ingest.py     |
| - chunk               |
| - embed (OpenAI)      |
| - add metadata        |
+----------------------+
        |
        v
+----------------------+
| Chroma Vector DB      |
| vectorstore/chroma    |
| collection=documents  |
+----------------------+
        ^
        |
+----------------------+
| FastAPI Service       |
| POST /api/v1/ask      |
| - embed query         |
| - top-K retrieval     |
| - build prompt        |
| - LLM answer          |
+----------------------+
        |
        v
Client (curl / app)
CI

GitHub Actions runs:

pytest

Docker build validation

What This Demonstrates

End-to-end RAG system design (ingest → embed → retrieve → generate)

Vector database integration and persistence

Grounded LLM answering with sources

Observability with tracing and latency instrumentation

Safe configuration management (guards + reset controls)

Containerized deployment and CI automation

Project Status

✔️ Ingestion + chunking working
✔️ OpenAI embeddings + Chroma persistence working
✔️ Retrieval + grounded LLM answering working
✔️ Logging/tracing + latency metrics working
✔️ Evaluation harness working
✔️ Docker container working with persisted vectorstore
✔️ CI pipeline working
✔️ Documentation complete

End of File