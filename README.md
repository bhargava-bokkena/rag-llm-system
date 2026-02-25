Project 2 — Production-Style RAG / LLM System

This project implements a complete production-style RAG (Retrieval-Augmented Generation) workflow, taking a document set from:
Ingestion → Chunking → Embeddings → Vector DB (Chroma) → Retrieval → LLM Answering → API Serving → Logging/Tracing → Evaluation → Docker → CI

It is designed to imitate how modern enterprise LLM/RAG systems are built.

Features

This project includes:

Document ingestion + deterministic chunking from data/raw/

OpenAI embeddings (default: text-embedding-3-small, 1536-dim)

Chroma vector database with persistent storage (vectorstore/chroma)

Retrieval pipeline (top-K) with sources + similarity distances

LLM answer synthesis grounded strictly in retrieved context

Request tracing + latency metrics (x-trace-id, x-duration-ms, plus stage metrics)

Evaluation harness (scripts/eval.py) for grounding + latency checks

Dockerized API service with persistent vectorstore volume mount

Pytest smoke tests

GitHub Actions CI (pytest + Docker build)

Safety guards: embedding model/dimension metadata + startup compatibility check

Operational controls: RESET_COLLECTION + COLLECTION_NAME for safe re-ingestion

How to Run Locally
Create virtual environment & install dependencies
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Create .env
cp .env.example .env

Set at minimum:

OPENAI_API_KEY=YOUR_KEY_HERE

(Optional but recommended defaults)

OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_DB_DIR=vectorstore/chroma
COLLECTION_NAME=documents
RESET_COLLECTION=false
Ingest documents into Chroma

Put .txt files into data/raw/, then run:

python -m scripts.ingest

This will:

load docs

chunk them

embed chunks

store in Chroma with metadata: source, doc_id, chunk_index, embedding_model, embedding_dim

Run FastAPI server locally
uvicorn app.main:app --reload --port 8000

Test endpoints:

curl http://127.0.0.1:8000/api/v1/health

Ask a question:

curl -X POST "http://127.0.0.1:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the internal knowledge base contain?","top_k":2}'

You will receive:

answer

sources (source path + distance)

metrics (retrieve_ms, llm_ms, total_ms)
And response headers:

x-trace-id

x-duration-ms

Evaluation

With the API running, run:

python -m scripts.eval

This outputs:

pass/fail checks

avg latency

per-question latency + top source

grounding behavior (“I don’t know” when context is missing)

Run with Docker
Build image
docker build -t rag-llm-system:latest .
Run container
docker run --rm -p 8000:8000 --env-file .env rag-llm-system:latest
Run container with persistent vector store
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  -v "$(pwd)/vectorstore/chroma:/app/vectorstore/chroma" \
  rag-llm-system:latest
Test
curl http://127.0.0.1:8000/api/v1/health
Architecture Overview

This project follows a clean RAG architecture with separate components for:

Ingestion (offline job)

Vector store (persistent DB)

Query pipeline (retrieve + synthesize)

Serving (FastAPI)

Observability (trace IDs + latency metrics)

Evaluation (repeatable checks)

Packaging (Docker)

CI (tests + docker build)

Components
Ingestion

Code: app/rag/ingestion.py and scripts/ingest.py

Loads docs from data/raw/

Chunks + metadata enrichment

Embeds with OpenAI embeddings

Stores in Chroma (vectorstore/chroma)

Supports operational controls:

COLLECTION_NAME

RESET_COLLECTION

Vector Store

Code: app/rag/vectorstore.py

Chroma persistent client

Collection-based storage

Retrieval + RAG

Retrieval: app/rag/retrieval.py

RAG orchestration: app/rag/__init__.py

LLM + embeddings client: app/rag/llm.py

Response returns sources + distances + stage metrics

Serving

FastAPI: app/main.py, app/api/v1/routes.py

Endpoints:

/api/v1/health

/api/v1/ask

Safety / Guardrails

Stores embedding_model + embedding_dim in metadata at ingest time

Startup compatibility guard fails fast if EMBEDDING_MODEL changed without re-ingestion

Guard code: app/rag/guards.py

High-Level Architecture Diagram (ASCII)
                 +----------------------+
                 |   data/raw/*.txt     |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |  Ingestion Job       |
                 |  scripts/ingest.py   |
                 |  - load + chunk      |
                 |  - embed (OpenAI)    |
                 |  - add metadata      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |  Chroma Vector DB    |
                 |  vectorstore/chroma  |
                 |  collection=documents|
                 +----------+-----------+
                            ^
                            |
        +-------------------+-------------------+
        |                                       |
        v                                       v
+----------------------+               +----------------------+
| FastAPI Service      |               | Evaluation Harness   |
| app.main + /ask      |               | scripts/eval.py      |
| - embed query        |               | - sends queries      |
| - top-K retrieval    |               | - checks grounding   |
| - build prompt       |               | - tracks latency     |
| - LLM answer         |               +----------------------+
+----------+-----------+
           |
           v
   +------------------+
   | Client / curl     |
   +------------------+
CI (GitHub Actions)

Workflow: .github/workflows/ci.yml

Runs:

pytest

Docker build validation

What I Learned / Skills Demonstrated
LLM / RAG Engineering

Building an end-to-end RAG pipeline (ingest → embed → retrieve → generate)

Designing grounded responses with explicit source context

Vector similarity search and retrieval tuning (top-K, distances)

Software Engineering

FastAPI microservice design

Structured logging, trace IDs, and request-level latency instrumentation

Clean module separation (ingestion vs query-time serving)

Testing & Evaluation

Pytest API smoke tests

Lightweight RAG evaluation harness (grounding + latency)

DevOps / Infrastructure

Dockerized deployment with persistent vectorstore volume mounts

CI automation via GitHub Actions

Operational controls for safe re-ingestion and configuration drift prevention

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