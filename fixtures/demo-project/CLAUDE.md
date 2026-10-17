# demo-project (repo guide for agents)

A tiny FastAPI + SQLite pantry API used as a fixture for testing the agent-toolkit.

## Layout
- `app/main.py` - `create_app(db_path)` factory and all endpoints
- `app/db.py` - sqlite3 data layer (table `items`)
- `app/server.py` - uvicorn entry point (`PANTRY_DB` env var)
- `tests/` - pytest tests; `scripts/e2e.sh` - HTTP smoke test
- `tickets/` - sample tickets in contract format

## Commands
- `make test` - unit tests; `make e2e` - HTTP smoke; `make verify` - both
- `make dev` - run on 127.0.0.1:8765 with a seeded db

## Conventions
- Keep it small and boring; stdlib plus fastapi only.
- Every ticket ends green on `make verify`.
- `PROGRESS.md` is append-only.
