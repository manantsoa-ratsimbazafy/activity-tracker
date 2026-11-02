# Activity Tracker

A REST API to track time sessions per activity, built with FastAPI and PostgreSQL.
A personal learning project focused on backend development, security and DevSecOps.

## Key rule
Only one open session (no end time) can exist per activity. This is enforced
by the database itself with a partial unique index, not just by application code.

## Tech stack
Python 3.13, FastAPI, SQLAlchemy 2.x, PostgreSQL, Pydantic, uv, pytest, ruff

## Getting started
Prerequisites: Python 3.13, uv, PostgreSQL.
1. Install dependencies: `uv sync`
2. Create PostgreSQL databases (both main and test, e.g. `activities_audit` and `activities_test`) with a dedicated non-superuser role assigned to both.
3. Copy `.env.example` to `.env` and fill in your values (`DATABASE_URL` and `TEST_DATABASE_URL`).
4. Initialize the database tables on your `DATABASE_URL`: `uv run python scripts/create_tables.py`
5. Run the API: `uv run uvicorn app.main:app --reload`, then open `/docs`

## Tests
Tests run against a separate database (`TEST_DATABASE_URL`). They refuse to
run if it equals `DATABASE_URL`. Run: `uv run pytest`

## Endpoints
| Method | Path | Success | Errors |
|---|---|---|---|
| GET | /health | 200 | |
| POST | /activities | 201 | 409, 422 |
| GET | /activities | 200 | 422 |
| GET | /activities/{id} | 200 | 404 |
| POST | /activities/{id}/start | 201 | 404, 409 |
| POST | /activities/{id}/stop | 200 | 404 |
| GET | /activities/{id}/entries | 200 | 404, 422 |

- Lists accept `limit` (1-100, default 10) and `offset` (>= 0).
- Activity names (`POST /activities`) must be from **1 to 20 characters** long (leading and trailing whitespace are automatically trimmed).

## Roadmap
- Docker containerization
- Trivy and Semgrep security scans
- Authentication and authorization