# Contributing

Notes on how the project is organized and the conventions I follow when working on it. Useful if you are reading the code or extending it.

## Project layout

- `app/models/` — SQLAlchemy ORM models
- `app/schemas/` — Pydantic request and response models
- `app/crud/` — database access and business logic; all queries live here
- `app/routers/` — route definitions, kept thin and delegating to `crud`
- `app/core/` — security and shared utilities
- `alembic/` — database migrations
- `seed/` — SQL seed data
- `tests/` — integration tests

## Code conventions

- Async SQLAlchemy 2.x only. Use `select()` with ORM and Core expressions; no synchronous sessions.
- Keep database work in `app/crud/`, not in routers.
- Every endpoint returns a Pydantic response model.
- Raise `HTTPException` with the right status code:
  - `400` for invalid input or a bad foreign key reference
  - `401` when no valid token is supplied
  - `403` when a token is valid but lacks admin rights
  - `404` when a resource does not exist
- Never hardcode secrets. Configuration comes from `.env`.

## Auth model

- All `GET` routes are public.
- `POST`, `PUT`, and `DELETE` require an admin token.
- Admin credentials come from `.env` (`ADMIN_USERNAME` and `ADMIN_PASSWORD_HASH`). See [DEVELOPMENT.md](DEVELOPMENT.md) for generating the password hash.
- Get a token from `POST /auth/login`, then send it as `Authorization: Bearer <token>`.

## Development workflow

The day-to-day commands for Docker, migrations, linting, tests, and seeding are in [DEVELOPMENT.md](DEVELOPMENT.md). The short version: bring up Docker, run `ruff check app tests`, and make sure `python -m pytest -v` is green before committing.

## Commit messages

Short, present-tense summaries with a type prefix:

- `feat: add publication authorship endpoints`
- `fix: return 404 for missing grant`
- `docs: refresh API reference`
- `chore: tidy comments`
- `test: cover viewer-token rejection`

Prefer small, focused commits over large mixed ones.

## Database schema

The models in `app/models/` are the source of truth for the schema. Table and column details are documented in [API.md](API.md).
