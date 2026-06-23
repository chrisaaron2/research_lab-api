# Research Lab Manager API

A FastAPI and PostgreSQL backend for managing a research lab's members, projects, grants, equipment usage, and publications. It started as a database systems course project and grew into a backend I keep as a portfolio piece: async SQLAlchemy models, JWT-protected write routes, reporting endpoints, deterministic seed data, integration tests, CI, and Dockerized local development.

## Overview

The system models a research lab as a relational database and exposes it through a REST API. Members (students, faculty, and collaborators) work on projects, projects are funded by grants, equipment contains devices, members log usage of those devices, and publications track authorship across the lab. Read routes are public; write routes require an admin token.

The backend is the completed core of the project. A React admin frontend is in early development and is covered under Roadmap.

## Why I built it

The original CS 631 (Databases) assignment asked for a practical system with sample data and useful operations: project and member management, equipment usage tracking, and grant and publication reporting. I wanted more than a schema with a few queries, so I rebuilt it as a real API with migrations, an auth layer, tests, and CI. It was a focused way to practice async FastAPI and relational design from the database up.

## Features

- Members API with student, faculty, and collaborator subtypes and a self-referential mentor relationship
- Projects, grants, equipment, devices, and equipment-usage records with full CRUD
- Publications with authorship management (add and remove authors per publication)
- Reporting endpoints using joins, grouping, aggregation, and date filtering
- JWT authentication with public reads and admin-only writes
- Deterministic seed data for a fully populated demo database
- Integration test suite and GitHub Actions CI
- Docker Compose setup for local Postgres and the API

## Tech Stack

- **API and runtime:** Python, FastAPI, Pydantic
- **Data:** PostgreSQL 16, SQLAlchemy 2.x (async), Alembic
- **Auth:** JWT via python-jose, password hashing via passlib/bcrypt
- **Testing and tooling:** Pytest, pytest-asyncio, httpx (ASGITransport), Ruff
- **Infrastructure:** Docker, Docker Compose, GitHub Actions

## Architecture

```
app/
  main.py            FastAPI app, router registration, health endpoint, CORS
  db.py              async engine and session dependency
  core/security.py   JWT, password hashing, admin dependency
  models/            SQLAlchemy ORM models
  schemas/           Pydantic request and response models
  crud/              data access and business logic
  routers/           route definitions per resource
alembic/             database migrations
seed/                SQL seed data
tests/               integration tests
docs/                API reference and development notes
```

Routers stay thin and delegate to the `crud` layer, which holds the queries and business rules. Pydantic schemas define request and response shapes; SQLAlchemy models define the tables and relationships.

## Data Model

Core tables and how they relate:

- `LAB_MEMBER` holds shared member fields. `STUDENT`, `FACULTY`, and `COLLABORATOR` are subtype tables with one-to-one links back to it. `LAB_MEMBER` also references itself for mentorship.
- `PROJECT` connects to members through the `WORKS` association table.
- `GRANT` links funding to a project.
- `EQUIPMENT` owns `DEVICE` records. `USES` tracks which member used which device, keyed by member, device, and equipment.
- `PUBLICATION` connects to authors through `PUBLISHES`.

Schema changes are managed with Alembic. The seed dataset loads 18 members (6 students, 6 faculty, 6 collaborators), 8 mentorships, 8 projects, 10 grants, 12 equipment records, 20 devices, 30 usage records, and 25 publications, along with the association rows.

## API Surface

Routes are grouped by resource. GET routes are public; POST, PUT, and DELETE require an admin token.

- **Health:** service status
- **Auth:** login for an admin token
- **Members:** list, detail, members by grant, project mentorships, plus admin CRUD
- **Projects:** list, detail, status, plus admin CRUD
- **Equipment:** list, detail, active users, plus admin CRUD
- **Devices:** list, detail, plus admin CRUD
- **Uses:** list and active-only filter, plus admin create, update, and delete by member/device/equipment
- **Grants:** list with filters (by project, by agency), detail, plus admin CRUD
- **Publications:** list with filters (year, venue, author), detail, authors, plus admin CRUD and author management
- **Reports:** see below
- **Admin seed:** load the seed dataset

Full request and response details are in [docs/API.md](docs/API.md).

## Authentication

`POST /auth/login` returns a JWT. Send it as `Authorization: Bearer <token>` on write routes. Public GET routes need no token. A non-admin token is rejected on protected routes, and a missing token returns 401.

## Reports

- `GET /reports/top-funded-projects`: projects ranked by total grant funding
- `GET /reports/top-mentors-by-publications`: mentors ranked by their mentees' publication counts
- `GET /reports/student-publications-by-major-year`: student publication counts grouped by major and year
- `GET /reports/projects-ended-before?date=YYYY-MM-DD`: projects that ended before a given date
- `GET /reports/top-publication-years`: years ranked by publication count

## Testing

The suite has 63 integration tests covering auth, members, projects, equipment, devices, usage, grants, publications and authorship, and reports. They run against the app through httpx's ASGITransport, so they exercise the real routing and database layer.

```powershell
python -m pytest -v
```

One known warning comes from python-jose calling `datetime.utcnow` internally. It does not affect results; moving to PyJWT is on the roadmap.

## Local Development

Developed on Windows with PowerShell. The Docker and Python commands are the same across platforms; adjust the virtual environment activation line for your shell.

```powershell
# Clone and enter the project
git clone https://github.com/<you>/research_lab-api.git
cd research_lab-api

# Create a virtual environment for local tooling (ruff, pytest)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# set SECRET_KEY and ADMIN_PASSWORD_HASH in .env

# Start PostgreSQL and the API
docker compose up -d

# Apply migrations, then load seed data
alembic upgrade head
# seed via POST /admin/seed (see docs/API.md) or seed/seed.sql

# Lint and test
ruff check app tests
python -m pytest -v
```

The API runs at `http://localhost:8000` with interactive docs at `/docs`.

## Example Requests

```bash
# Log in and capture a token
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "<your-password>"}'

# Public read
curl "http://localhost:8000/publications?year=2024"

# Admin write (request body shapes are in docs/API.md)
curl -X POST http://localhost:8000/members \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

## Documentation

- [docs/API.md](docs/API.md): full API reference
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): local development notes

## Current Status

- **Backend API:** complete through members, projects, equipment, devices, usage, grants, publications and authorship, reporting, auth, tests, CI, and docs.
- **Frontend admin dashboard:** in early development.
- **Deployment:** runs locally; not yet hosted.

## Roadmap

- Build out the React admin pages for projects, grants, equipment, devices, usage, publications, and reports
- Add pagination and server-side search to list endpoints
- Add audit logging for admin changes
- Add finer-grained, role-based permissions
- Replace python-jose with PyJWT to clear the deprecation warning
- Deploy the backend and frontend
- Add dashboard charts once the admin pages are in place

## What This Demonstrates

- Relational schema design with subtype and association tables
- Async FastAPI development with a clean router, schema, and CRUD separation
- SQLAlchemy ORM modeling and Alembic migrations
- PostgreSQL query design for reports: joins, grouping, aggregation, and date filtering
- JWT-protected routes with a public read and admin write split
- CRUD workflows with validation and dependency handling
- Deterministic seed data for reproducible local runs
- Integration testing and GitHub Actions CI
- Dockerized local development
