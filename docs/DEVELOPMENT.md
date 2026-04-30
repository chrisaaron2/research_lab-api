# Development Guide

This guide uses PowerShell examples because the project is developed on Windows.

## Daily Workflow

```powershell
.\.venv\Scripts\Activate.ps1
git status --short
docker compose up -d
ruff check app tests
python -m pytest -v
git status --short
```

When the checks pass:

```powershell
git add .
git commit -m "Describe the change"
git push
```

## Docker Workflow

Start or rebuild services:

```powershell
docker compose up -d --build
```

Check service status:

```powershell
docker compose ps
```

View API logs:

```powershell
docker compose logs api
```

Stop services:

```powershell
docker compose down
```

## Database Workflow

Create a migration after changing models:

```powershell
alembic revision --autogenerate -m "message"
```

Apply migrations:

```powershell
alembic upgrade head
```

Open `psql` inside the database container:

```powershell
docker compose exec db psql -U postgres -d lab_db
```

## Testing Workflow

Run linting:

```powershell
ruff check app tests
```

Run tests:

```powershell
python -m pytest -v
```

The test fixtures run Alembic, reset application tables, and load `seed/seed.sql`
automatically. Tests use the PostgreSQL database configured by
`TEST_DATABASE_URL`.

## Auth Workflow

Generate a local secret key with a password manager or another secure random
source, then place it in `.env`:

```env
SECRET_KEY=replace-with-generated-secret
```

Generate a bcrypt password hash in a local Python shell:

```powershell
python
```

```python
from app.core.security import get_password_hash
get_password_hash("admin123")
```

Put the resulting hash in `.env`:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH='replace-with-bcrypt-hash'
```

Quoting the hash avoids confusion with `$` characters inside bcrypt hashes.

Do not commit `.env`.

## Git Workflow

Check changes:

```powershell
git status --short
```

Stage and commit:

```powershell
git add .
git commit -m "Describe the change"
```

Push:

```powershell
git push
```

## Troubleshooting

### bcrypt/passlib warning or compatibility issue

The project pins bcrypt compatibility through `bcrypt==4.0.1`.

### Protected route returns missing bearer token

Login first and pass the token in the `Authorization` header:

```powershell
$login = Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/auth/login `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'

$headers = @{ Authorization = "Bearer $($login.access_token)" }
```

### Tests cannot connect to the database

Check that PostgreSQL is running:

```powershell
docker compose ps
```

Start it if needed:

```powershell
docker compose up -d
```

### Docker app does not reflect changes

Rebuild the image:

```powershell
docker compose up -d --build
```

### `.env` appears in git status

Do not commit it. `.env` should remain local only.
