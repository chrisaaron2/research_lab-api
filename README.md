# Research Lab Manager API

A FastAPI + PostgreSQL backend for managing research lab members, projects,
grants, equipment, device usage, publications, and reports.

This project is built as a production-style backend portfolio project with async
database access, JWT-protected write routes, integration tests, and CI.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x async ORM
- Alembic
- Pydantic
- JWT auth with python-jose
- Passlib/bcrypt
- Docker Compose
- Pytest
- Ruff
- GitHub Actions

## Features

- Lab member management with student, faculty, and collaborator subtypes
- Project management and project status tracking
- Grant CRUD and grant-funded project/member queries
- Equipment, device, and usage tracking
- Active equipment users with project context
- Publication and funding reports
- JWT-protected write routes
- Seed data loading
- Integration tests and CI

## Project Structure

```text
app/
  models/
  schemas/
  crud/
  routers/
  core/
alembic/
seed/
tests/
.github/workflows/
```

- `app/`: FastAPI application package.
- `app/models/`: SQLAlchemy ORM models.
- `app/schemas/`: Pydantic request and response models.
- `app/crud/`: Database query and mutation logic.
- `app/routers/`: API route definitions.
- `app/core/`: Shared core helpers such as JWT security.
- `alembic/`: Database migration environment.
- `seed/`: Deterministic sample SQL data.
- `tests/`: Async integration tests.
- `.github/workflows/`: GitHub Actions CI workflow.

## Environment Variables

Required variables:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/lab_db
SECRET_KEY=replace-with-generated-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=replace-with-bcrypt-hash
```

`.env` is local only and must not be committed. `.env.example` contains
placeholder values. Use host `db` when the FastAPI app runs inside Docker
Compose. Use `localhost` only for local commands or tests that run directly from
your machine.

## Local Setup

```powershell
git clone <repository-url>
cd research_lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d --build
```

## Database Setup

PostgreSQL runs through Docker Compose. Alembic manages schema migrations.

```powershell
alembic upgrade head
```

After authentication is configured, seed data is loaded through
`POST /admin/seed` with a Bearer token. See the Authentication section below for
a PowerShell example. Tests reset and seed the database automatically.

## Authentication

Public `GET` routes do not require auth. `POST`, `PUT`, and `DELETE` routes
require a Bearer token.

Login endpoint:

```text
POST /auth/login
```

PowerShell example:

```powershell
$login = Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/auth/login `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'

$headers = @{ Authorization = "Bearer $($login.access_token)" }

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/admin/seed `
  -Headers $headers
```

`admin/admin123` is only a local example. The actual admin password is controlled
by `ADMIN_PASSWORD_HASH`.

## Running the API

- API base URL: `http://localhost:8000`
- FastAPI docs: `http://localhost:8000/docs`
- Health check: `GET /health`

## Frontend Demo Dashboard

The demo dashboard lives in `frontend/` and runs separately from the FastAPI
backend.

```powershell
cd frontend
npm install
npm run dev
```

Build the frontend with:

```powershell
npm run build
```

- Frontend URL: `http://localhost:5173`
- Backend URL: `http://localhost:8000`
- FastAPI docs: `http://localhost:8000/docs`
- Override the API URL with `VITE_API_BASE_URL` if needed.

Demo login:

- Username: `admin`
- Password: `admin123`

## Running Tests

```powershell
ruff check app tests
python -m pytest -v
```

Current test suite:

- 36 integration tests
- Auth, members, projects, equipment/devices/uses, and reports

## CI

GitHub Actions runs on `push` and `pull_request`. The workflow starts
PostgreSQL 16, installs dependencies, runs Ruff, and runs pytest.

## Main API Areas

- Auth: login and JWT creation
- Admin: seed data loading
- Members: lab members and subtypes
- Projects: project CRUD and status
- Equipment: equipment inventory
- Devices: physical device records
- Uses: member usage of devices/equipment
- Reports: grant funding and publication analytics

## Notes / Known Warnings

`python-jose` may emit a `datetime.utcnow` deprecation warning during tests. The
warning comes from the dependency and does not fail the test suite.

## Future Improvements

- Minimal UI dashboard
- Role-based users beyond a single admin
- Deployment
- More granular permissions
- Pagination and filtering enhancements
- Coverage threshold
