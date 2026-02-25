Production-Style RAG / LLM System

This project implements a complete production-style RAG (Retrieval-Augmented Generation) workflow, taking a document set from:

Ingestion → Chunking → Embeddings → Vector DB (Chroma) → Retrieval → LLM Answering → API Serving → Logging/Tracing → Evaluation → Docker → CI

It is designed to imitate how modern enterprise LLM/RAG systems are built.

Features

This project includes:

Document ingestion + deterministic chunking (data/raw/)

OpenAI embeddings (text-embedding-3-small, 1536-dim)

Chroma vector database with persistent storage

Retrieval pipeline (top-K) with sources + similarity distances

LLM answer synthesis grounded strictly in retrieved context

Request tracing + latency metrics (x-trace-id, x-duration-ms)

Evaluation harness (scripts/eval.py)

Dockerized API service

Pytest smoke tests

GitHub Actions CI (pytest + Docker build)

Startup compatibility guard for embedding drift

Operational controls: RESET_COLLECTION + COLLECTION_NAME

How to Run Locally
Create virtual environment & install dependencies
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Create .env
cp .env.example .env

Set at minimum:

OPENAI_API_KEY=YOUR_KEY_HERE

Optional defaults:

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

Outputs:

Pass/fail checks

Average latency

Per-query metrics

Grounding validation

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
        │
        ▼
+------------------+
| Ingestion Job    |
| - chunk          |
| - embed          |
| - metadata       |
+------------------+
        │
        ▼
+------------------+
| Chroma Vector DB |
| collection=docs  |
+------------------+
        ▲
        │
+------------------+
| FastAPI Service  |
| /api/v1/ask      |
| - embed query    |
| - top-K search   |
| - build prompt   |
| - LLM answer     |
+------------------+
        │
        ▼
Client / curl
CI

GitHub Actions runs:

pytest

Docker build validation

What This Demonstrates

End-to-end RAG system design

Vector database integration

LLM grounding discipline

Observability instrumentation

Safe configuration management

Containerized deployment

CI validation

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