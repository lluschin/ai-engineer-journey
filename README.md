# AI Engineer Journey 🚀

*A modular AI engineering playground for building, evaluating and benchmarking Retrieval-Augmented Generation (RAG) systems.*

---

## Overview

This repository contains a modular AI engineering playground for designing, evaluating and benchmarking Retrieval-Augmented Generation (RAG) systems.

Instead of relying on high-level frameworks, the project focuses on understanding the individual building blocks of production-ready RAG systems, their responsibilities, trade-offs and evaluation strategies.

The architecture is intentionally modular to allow different AI components to be exchanged, benchmarked and evaluated independently.

---

## Current Features

### LLM Providers

* OpenAI
* Ollama (local models)

### Embedding Providers

* OpenAI Embeddings
* Ollama Embeddings

### Vector Database

* Qdrant

### Retrieval Pipeline

* Configurable Top-K Retrieval
* Provider abstraction
* Chunking
* Heuristic Re-Ranking
* Context Building

### Evaluation

* Automated benchmark suite
* Multiple model comparison
* Retrieval benchmarking
* Runtime measurement

### Architecture

* Provider-independent services
* Service Registry
* Configuration-driven experiments
* Modular pipeline
* FastAPI backend

---

# Architecture

```text
                 Client
                    │
                FastAPI API
                    │
             Service Registry
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
  Retrieval Service        LLM Service
        │
        ▼
     Ranker
        │
        ▼
 Context Builder
        │
        ▼
     Qdrant
```

---

# Project Goals

This project focuses on understanding and implementing the engineering aspects behind modern AI applications.

Current topics include:

* Retrieval-Augmented Generation (RAG)
* Embedding Models
* Vector Databases
* Chunking Strategies
* Re-Ranking
* Context Engineering
* Prompt Engineering
* Evaluation & Benchmarking
* Modular Software Architecture

Future topics include:

* Hybrid Search
* Cross-Encoder Re-Ranking
* Retrieval Metrics (Recall@K, Precision@K, MRR)
* AWS Bedrock
* Agentic Workflows
* MCP (Model Context Protocol)
* Multi-Agent Systems
* Production Deployment

---

# Tech Stack

| Component       | Technology             |
| --------------- | ---------------------- |
| Backend         | FastAPI                |
| LLMs            | OpenAI, Ollama         |
| Embeddings      | OpenAI, Ollama         |
| Vector Database | Qdrant                 |
| Language        | Python                 |
| Configuration   | TOML                   |
| Evaluation      | Custom Benchmark Suite |

---

# Design Principles

The project follows several software engineering principles:

* Separation of Concerns
* Provider Abstraction
* Dependency Inversion
* Configuration over Hardcoding
* Modular Pipelines
* Reproducible Experiments
* Continuous Evaluation

---

# Roadmap

## ✅ Version 1.0

* FastAPI Backend
* Provider Abstraction
* OpenAI & Ollama
* Qdrant Integration
* Chunking
* Retrieval Pipeline
* Heuristic Ranking
* Context Builder
* Evaluation Framework
* Benchmarking
* Service Registry

## 🚧 Next

* Retrieval Metrics
* Hybrid Search
* Cross-Encoder Ranking
* Context Compression
* AWS Bedrock
* Agentic Workflows

---

# Why this repository?

The objective is not to build another chatbot.

The objective is to understand how modern AI systems are engineered, evaluated and continuously improved.

Every architectural decision is intentionally designed to keep the system modular, measurable and extensible.

---

## License

MIT
