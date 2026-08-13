# SupportPilot AI Engine

Independently deployable Python service for AI workloads (classification, RAG, agent orchestration).

## Prerequisites

- Python 3.12+ (use [uv](https://docs.astral.sh/uv/) if your system Python is older)
- pip or uv

## Setup

```bash
cd services/ai-engine

# Option A: uv (recommended if Python 3.12 is not installed system-wide)
uv venv --python 3.12 .venv
uv pip install -e ".[dev]"

# Option B: standard venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tests

```bash
pytest
```

## Lint

```bash
ruff check .
```

## Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok", "service": "ai-engine"}
```
