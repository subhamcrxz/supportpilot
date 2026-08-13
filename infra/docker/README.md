# Docker infrastructure for local development.

PostgreSQL and Redis are defined in the root `docker-compose.yml`.

## PostgreSQL

Uses the `pgvector/pgvector:pg16` image — pgvector extension is available for future RAG/embedding work. No application schema is applied yet.

Connection string (default):

```
postgresql://supportpilot:supportpilot@localhost:5432/supportpilot
```

## Redis

Default connection:

```
redis://localhost:6379
```

## Usage

From the repository root:

```bash
docker compose up -d
docker compose ps
docker compose down
```
