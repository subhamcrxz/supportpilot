# SupportPilot

AI-powered support operations platform for small and mid-sized B2B SaaS companies.

## What is SupportPilot?

SupportPilot helps SaaS support teams automate repetitive support work — ticket classification, draft responses, knowledge retrieval — while keeping humans in control for uncertain or sensitive cases.

## Architecture

```
Web (Next.js)  →  API (Fastify)  →  AI Engine (FastAPI)
                        ↓
                  PostgreSQL + Redis
```

- **Web** — Next.js App Router frontend
- **API** — TypeScript/Fastify backend for business logic and integrations
- **AI Engine** — Python/FastAPI service for AI workloads (independently deployable)
- **Infrastructure** — PostgreSQL (with pgvector) and Redis via Docker Compose

See [docs/architecture/README.md](docs/architecture/README.md) for details.

## Prerequisites

- **Node.js** 20+
- **pnpm** 9+ (`corepack enable && corepack prepare pnpm@latest --activate`)
- **Python** 3.12+
- **Docker** and Docker Compose (for PostgreSQL and Redis)

## Installation

```bash
pnpm install
```

Copy environment variables:

```bash
cp .env.example .env
```

### AI Engine (Python)

```bash
cd services/ai-engine
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development

Start all TypeScript apps (web + API):

```bash
pnpm dev
```

Individual services:

```bash
# Web (http://localhost:3000)
pnpm --filter @supportpilot/web dev

# API (http://localhost:3001)
pnpm --filter @supportpilot/api dev

# AI Engine (http://localhost:8000)
cd services/ai-engine && uvicorn app.main:app --reload --port 8000
```

Start infrastructure:

```bash
docker compose up -d
```

## Commands

| Command | Description |
|---------|-------------|
| `pnpm install` | Install all workspace dependencies |
| `pnpm dev` | Start web and API in development mode |
| `pnpm build` | Build all TypeScript packages and apps |
| `pnpm lint` | Lint all TypeScript packages and apps |
| `pnpm test` | Run tests (API + AI engine) |

## Project Structure

```
supportpilot/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # Fastify API
├── services/
│   └── ai-engine/    # Python FastAPI AI service
├── packages/
│   ├── types/        # Shared TypeScript types
│   ├── config/       # Shared configuration utilities
│   └── prompts/      # Version-controlled AI prompts
├── evals/            # AI evaluation datasets and results
├── docs/             # Architecture and product documentation
└── infra/docker/     # Docker infrastructure notes
```

## Health Endpoints

| Service | URL |
|---------|-----|
| Web | http://localhost:3000 |
| API | http://localhost:3001/health |
| AI Engine | http://localhost:8000/health |

## Current Status

**Initial monorepo foundation.**

Implemented: workspace tooling, health endpoints, minimal web homepage with service status checks, Docker Compose for PostgreSQL + Redis.

Not yet implemented: authentication, billing, ticket management, integrations, RAG, AI agents, database schema.
