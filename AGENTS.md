\# Research Lab Manager — Agent Instructions



\## Project Overview

A FastAPI REST API for a Research Lab Manager system. Academic project for CS 631 at NJIT, built to production-grade standards as a portfolio project targeting SWE/backend roles.



\## Stack

\- FastAPI (async)

\- SQLAlchemy 2.x with async sessions

\- Alembic for migrations

\- PostgreSQL 16

\- Docker Compose

\- python-jose for JWT

\- passlib\[bcrypt] for password hashing

\- pytest + httpx for async integration testing

\- GitHub Actions

\- ruff



\## Key Conventions

\- All DB operations go in `app/crud/`

\- All SQLAlchemy models go in `app/models/`

\- All Pydantic schemas go in `app/schemas/`

\- All routers go in `app/routers/`

\- Use SQLAlchemy 2.x async style only

\- Use `select()` and ORM/Core expressions

\- Never use synchronous SQLAlchemy

\- Never hardcode secrets

\- All responses must use Pydantic response models

\- Use `HTTPException` with correct status codes

\- 404 for not found

\- 401 for unauthenticated

\- 403 for unauthorized



\## Auth Rules

\- All GET routes are public

\- All POST, PUT, DELETE routes require admin auth

\- Seed users later:

&#x20; - admin / lab\_admin123

&#x20; - viewer / lab\_viewer123



\## Project Rules

\- Do not add features outside the requested phase

\- Before running shell commands, explain what will be run

\- Keep code modular and production-style

\- Prefer small focused edits over large rewrites



\## Database Schema

LAB\_MEMBER (MID, NAME, JOIN\_DATE, TYPE, MENTOR self-ref FK, M\_SDATE, M\_EDATE)

STUDENT (MID FK, SID unique secondary key, LEVEL, MAJOR)

COLLABORATOR (MID FK, AFFILIATION, CV)

FACULTY (MID FK, DEPARTMENT)

PROJECT (PID, TITLE, S\_DATE, E\_DATE, E\_DURATION, LEADER FK→MID)

WORKS (PID, MID, ROLE, HOURS) — composite PK

GRANT (GID, P\_DURATION, AGENCY, BUDGET, START\_DATE, PID FK→PROJECT)

EQUIPMENT (EID, E\_TYPE, E\_NAME, MANUAL)

DEVICE (DID, EID FK, STATUS, P\_DATE)

USES (MID, DID, EID, S\_DATE, E\_DATE, PURPOSE) — 3-way composite PK

PUBLICATION (PUBID, TITLE, VENUE, DATE, DOI)

PUBLISHES (MID, PUBID) — composite PK

