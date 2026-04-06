# Industrial Revenue & Growth Engine

A industrial-grade AI system for dynamic pricing, lead generation, compliance validation, and auditability.

<img width="1895" height="867" alt="image" src="https://github.com/user-attachments/assets/2b6a340d-345e-478b-bc28-06d176bbec1a" />


## Backend: https://industrial-backend-data.onrender.com/

## Front end live demo: https://industrial-revenue-growth-engine.lovable.app/

<img width="1898" height="831" alt="image" src="https://github.com/user-attachments/assets/5e966a95-05ec-4c8c-964b-150723f8bcdb" />


## Highlights

- FastAPI backend with JWT RBAC
- SQL Server ETL for pricing intelligence
- Lead enrichment and ethical scraping pipeline
- Local vector memory with ChromaDB
- LangGraph orchestration for agent workflows
- Local Hugging Face LLM loader with 4-bit/8-bit quantization
- Structured logs and Prometheus metrics

<img width="1910" height="853" alt="image" src="https://github.com/user-attachments/assets/55cd79c6-4205-45b6-8098-392f2b0e13cc" />


# Industrial Revenue & Growth Engine

## Overview

**Industrial Revenue & Growth Engine** is a production-grade, local-first AI platform designed to optimize pricing strategies, automate lead generation, and ensure compliance through auditable AI agent orchestration.

This system is built for industrial environments where **traceability, reliability, and data sovereignty** are critical. It integrates structured data (SQL Server), unstructured insights (vector databases), and local LLM inference to deliver actionable business decisions.

---

<img width="1895" height="860" alt="image" src="https://github.com/user-attachments/assets/d13a42a0-7a06-47d1-a539-bb7dde592090" />


## Key Capabilities

* Dynamic Pricing Optimization powered by AI agents
* Automated Lead Generation & Enrichment pipelines
* Compliance validation with full audit trail
* Local LLM execution (no external API dependency)
* Agent orchestration with deterministic workflows
* Enterprise-ready observability and logging

---

## Architecture

The system follows a **modular, agent-driven architecture**:

```
                ┌──────────────────────────────┐
                │        Frontend (React)      │
                │      Control Tower UI        │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │        FastAPI Backend       │
                │  (Auth, Routing, Middleware) │
                └──────────────┬───────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌───────────────┐   ┌────────────────────┐   ┌────────────────────┐
│ SQL Server    │   │ Vector DB          │   │ Observability Stack │
│ (Pricing Data)│   │ (Chroma / Qdrant)  │   │ (Logs, Metrics)     │
└───────────────┘   └────────────────────┘   └────────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │     AI Agent Orchestration   │
                │         (LangGraph)          │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │      Local LLM Inference     │
                │ (Transformers / Ollama)      │
                └──────────────────────────────┘
```

---

## AI Agent System

The platform uses **role-based AI agents**, orchestrated through LangGraph workflows:

### 1. Pricing Analyst Agent

* Analyzes historical pricing and sales data
* Performs feature engineering
* Simulates pricing scenarios
* Suggests optimal pricing strategies

### 2. Lead Scout Agent

* Executes scraping and API integrations
* Enriches lead data
* Stores semantic representations in vector DB
* Enables contextual retrieval for future campaigns

### 3. Compliance & Audit Agent

* Validates decisions against business rules
* Ensures regulatory compliance
* Logs all actions with full lineage
* Acts as a governance layer over AI decisions

---

## Technology Stack

### Backend

* FastAPI (async, high-performance API layer)
* Python (core business logic)
* JWT Authentication (secure access control)

### AI & LLM

* Hugging Face Transformers
* Quantization with bitsandbytes (4-bit / 8-bit)
* LangGraph (agent orchestration)
* Optional: Ollama / LocalAI for simplified local serving

### Data Layer

* SQL Server (Dockerized) for structured data
* ChromaDB or Qdrant for vector storage

### Observability

* Structured logging (JSON)
* Middleware-based latency tracking
* ELK Stack / Prometheus-ready metrics

### DevOps

* Docker & Docker Compose
* Local-first deployment
* GPU-aware configuration

---

## Project Structure

```
industrial_revenue_growth_engine/
│
├── app/
│   ├── api/                # FastAPI routes
│   ├── core/               # Config, security, middleware
│   ├── agents/             # AI agents (roles & prompts)
│   ├── services/           # Business logic (pricing, leads)
│   ├── db/                 # DB connections & models
│   └── main.py             # App entrypoint
│
├── data/
│   ├── etl/                # Data pipelines
│   └── seeds/              # Initial datasets
│
├── models/
│   └── hf_loader.py        # Local LLM loader
│
├── infra/
│   ├── docker-compose.yml  # Infrastructure services
│   └── prometheus.yml
│
├── frontend/               # React Control Tower (optional)
├── tests/                  # Unit & integration tests
├── .env.example
└── README.md
```

---

## Data Flow

1. Data is extracted from SQL Server via ETL pipelines
2. Feature engineering is applied for pricing models
3. AI agents analyze and generate decisions
4. Compliance agent validates outputs
5. Results are logged and persisted
6. Leads are enriched and stored in vector DB
7. Future queries leverage semantic retrieval

---

## Security Model

* JWT-based authentication
* Role-Based Access Control (RBAC)
* Middleware validation for all endpoints
* Secure agent execution boundaries

---

## Observability & Audit

* Every AI decision is logged
* Full traceability of pricing changes
* Audit logs stored in dedicated tables
* Metrics exposed for monitoring tools

---

## Local Deployment

### Requirements

* Docker & Docker Compose
* Python 3.10+
* GPU (recommended for LLM inference)

### Run the system

```bash
docker-compose up --build
```

### Start backend

```bash
uvicorn app.main:app --reload
```

---

## Performance Considerations

* Use quantized models (4-bit / 8-bit) to reduce VRAM usage
* Cache embeddings to avoid recomputation
* Optimize SQL queries with indexing strategies
* Run async pipelines for I/O-bound tasks

---

## Use Cases

* Industrial pricing optimization
* B2B lead generation at scale
* Revenue growth analytics
* AI-assisted decision governance


---

## Author

Federico Guillermo Gravina: AI & Data Engineering Architecture

---

## Final Notes

This project is designed with a strong focus on **production readiness**, ensuring that AI-driven decisions are not only powerful but also **transparent, auditable, and aligned with business constraints**.

It provides a solid foundation for building industrial-grade AI systems locally, without dependency on external services.

