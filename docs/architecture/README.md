# Architecture

SupportPilot follows a layered architecture with clear service boundaries.

```
Web
 ↓
API
 ↓
AI Engine
 ↓
Database
 ↓
External integrations
```

## Components

| Layer | Technology | Role |
|-------|-----------|------|
| **Web** | Next.js | Customer-facing UI and internal support dashboards |
| **API** | Fastify | Business logic, orchestration, integrations |
| **AI Engine** | FastAPI (Python) | AI workloads — classification, RAG, agent logic |
| **Database** | PostgreSQL | Persistent data (schema TBD) |
| **Cache** | Redis | Sessions, queues, rate limiting (future) |

## AI Engine Separation

The AI Engine is intentionally separated from the main API. AI workloads — model calls, embeddings, prompt execution, evaluation pipelines — have different scaling, deployment, and iteration requirements than CRUD and integration logic.

This separation allows:

- Independent deployment and scaling of AI services
- Python-native tooling for ML/AI libraries
- Prompt and model changes without redeploying the API
- Isolated failure domains for AI processing

## Current Status

Initial monorepo foundation. No database schema, authentication, or AI functionality implemented yet.
