Production-Style RAG / LLM System

This project implements a complete production-style RAG (Retrieval-Augmented Generation) workflow, taking a document set from:

Ingestion → Chunking → Embeddings → Vector DB (Chroma) → Retrieval → LLM Answering → API Serving → Logging/Tracing → Evaluation → Docker → CI

It is designed to imitate how modern enterprise LLM/RAG systems are built.

Features

This project includes:

Document ingestion and deterministic chunking from data/raw/

OpenAI embeddings (text-embedding-3-small, 1536-dim)

Chroma vector database with persistent storage (vectorstore/chroma)

Retrieval pipeline (top-K) with sources and similarity distances

LLM answer synthesis grounded strictly in retrieved context

Request tracing and latency metrics

Evaluation harness (scripts/eval.py)

Dockerized API service with persistent vectorstore volume mount

Pytest smoke tests

GitHub Actions CI pipeline

Embedding compatibility guard to prevent dimension mismatch

Operational controls: RESET_COLLECTION and COLLECTION_NAME

How to Run Locally
1. Set up virtual environment and install dependencies
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Create environment variables
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
3. Ingest documents

Put .txt files into data/raw/, then run:

python -m scripts.ingest

This will:

Load documents

Chunk text

Generate embeddings

Store vectors in Chroma with metadata

4. Run the FastAPI service
uvicorn app.main:app --reload --port 8000

Health check:

curl http://127.0.0.1:8000/api/v1/health

Ask a question:

curl -X POST "http://127.0.0.1:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the internal knowledge base contain?","top_k":2}'
5. Run evaluation harness
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
Run with persistent vectorstore
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  -v "$(pwd)/vectorstore/chroma:/app/vectorstore/chroma" \
  rag-llm-system:latest
Architecture Overview

This project follows a clean RAG architecture with dedicated components for:

Document ingestion

Vector storage

Retrieval pipeline

LLM answer synthesis

API serving

Observability and tracing

Evaluation

Containerized deployment

CI validation

High-Level Architecture Diagram
Components
Ingestion

Loads raw documents

Chunks text deterministically

Generates OpenAI embeddings

Stores metadata including embedding model and dimension

Vector Store

Chroma persistent client

Collection-based storage

Startup compatibility guard

Retrieval + RAG

Query embedding

Top-K similarity search

Context-grounded LLM answer synthesis

Serving

FastAPI application

Structured logging

Trace IDs and latency metrics

CI Automation

GitHub Actions workflow

Pytest execution

Docker build validation

What I Learned / Skills Demonstrated
LLM Engineering

Designing end-to-end RAG systems

Implementing vector search and retrieval

Enforcing grounded LLM answering

Software Engineering

Building modular API services with FastAPI

Adding observability and performance metrics

Managing configuration safely

DevOps / CI/CD

Dockerizing services

Persisting vector databases

Automating validation via GitHub Actions

Project Status

Ingestion pipeline implemented

Vector persistence operational

Retrieval and grounded answering functional

Logging and tracing implemented

Evaluation harness operational

Docker deployment working

CI pipeline functional

Documentation complete

End of File