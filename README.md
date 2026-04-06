# Industrial Revenue & Growth Engine

A local, industrial-grade AI system for dynamic pricing, lead generation, compliance validation, and auditability.

## Highlights

- FastAPI backend with JWT RBAC
- SQL Server ETL for pricing intelligence
- Lead enrichment and ethical scraping pipeline
- Local vector memory with ChromaDB
- LangGraph orchestration for agent workflows
- Local Hugging Face LLM loader with 4-bit/8-bit quantization
- Structured logs and Prometheus metrics

## Run

1. Copy `.env.example` to `.env`
2. Start the stack:

```bash
docker compose up -d --build
```

3. Open the API at `http://localhost:8000`
