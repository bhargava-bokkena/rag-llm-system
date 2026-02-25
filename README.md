Production-Style RAG / LLM System

A production-style Retrieval-Augmented Generation (RAG) microservice built with:

OpenAI embeddings

Chroma vector database

FastAPI

Structured logging and tracing

Evaluation harness

Docker

GitHub Actions CI

Overview

This project implements an end-to-end RAG pipeline designed to resemble a real enterprise AI microservice.

It ingests internal documentation, stores vector embeddings, retrieves relevant context at query time, and generates grounded LLM responses — with observability, persistence, and evaluation.

Architecture
1. Ingestion Layer

Load .txt documents from data/raw/

Chunk text deterministically

Generate OpenAI embeddings (text-embedding-3-small, 1536-dim)

Persist vectors into Chroma

Store embedding metadata (embedding_model, embedding_dim) to prevent dimension mismatches

Run ingestion:

python -m scripts.ingest
2. Query (RAG) Pipeline

On each request:

Embed user query

Perform top-K vector similarity search

Build grounded prompt using retrieved context

Call LLM for response synthesis

Return:

Answer

Source documents

Similarity distances

Latency metrics

API endpoint:

POST /api/v1/ask

Example:

curl -X POST "http://127.0.0.1:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the internal knowledge base contain?","top_k":2}'
Observability

Each request includes:

x-trace-id

x-duration-ms

Response JSON includes stage metrics:

retrieve_ms

llm_ms

total_ms

Structured logging enables trace-level debugging and latency inspection.

Evaluation

Run:

python -m scripts.eval

The evaluation script:

Runs a small test suite

Validates grounding behavior

Checks fallback responses

Measures latency

Reports pass rate

Docker Deployment

Build image:

docker build -t rag-llm-system:latest .

Run container:

docker run --rm -p 8000:8000 --env-file .env rag-llm-system:latest

Run with persistent vector store:

docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  -v "$(pwd)/vectorstore/chroma:/app/vectorstore/chroma" \
  rag-llm-system:latest
Tests

Run tests:

pytest -q

CI validates:

Unit tests

Docker build

Engineering Notes

Resolved embedding dimension mismatch (384 vs 1536) when switching embedding providers

Added embedding model and dimension metadata guard

Implemented request tracing and latency instrumentation

Separated ingestion from query service (production-style architecture)

Built evaluation harness for grounding validation

Tech Stack

Python 3.11

FastAPI

Chroma

OpenAI API

Docker

GitHub Actions