# Base FastAPI Application

A minimal, production-ready FastAPI starter with async PostgreSQL access, Alembic migrations, an admin panel, structured error handling, and Docker-based deployment.

## Features

- **FastAPI** app with async request handling (`uvloop`)
- **PostgreSQL** via `SQLAlchemy` (async) + `asyncpg`
- **Alembic** migrations, run automatically on container startup
- **SQLAdmin** admin panel with JWT-based, Argon2-hashed password authentication
- **Structured error responses** via a custom `AppError` hierarchy (`BadRequestError`, `UnauthorizedError`, `AccessDeniedError`, `NotFoundError`, `LimitExceededError`, `InternalServerError`)
- **CORS** configuration via environment variables
- **Sentry** integration ready (via `sentry-sdk`)
- **Docker Compose** setup with PostgreSQL and health checks
- Code quality tooling: `black`, `isort`, `autoflake`

## Project Structure

```
app/
├── admin/         # SQLAdmin views
├── crud/          # Database access layer
├── models/        # SQLAlchemy models
├── routers/       # API route definitions
├── schemas/       # Pydantic schemas
├── utils/         # DB session manager, exceptions, auth, helpers
├── config.py      # App settings (pydantic-settings)
├── dependencies.py
└── main.py        # App entrypoint / FastAPI instance
alembic/           # Database migrations
static/templates/  # Admin panel templates
```

## Requirements

- Python 3.12
- PostgreSQL 16
- Docker & Docker Compose (for containerized setup)

## Getting Started

### 1. Configure environment variables

Copy the example file and adjust the values:

```bash
cp .env.example .env
```

| Variable              | Description                                      | Default                 |
|-----------------------|---------------------------------------------------|--------------------------|
| `POSTGRES_DB`          | PostgreSQL database name                           | `master`                |
| `POSTGRES_USER`        | PostgreSQL user                                    | `user`                   |
| `POSTGRES_PASSWORD`    | PostgreSQL password                                | `password`               |
| `PG_DSN`               | Async SQLAlchemy DSN                               | -                        |
| `PG_ECHO`              | Log SQL statements                                 | `false`                  |
| `ADMIN_PASSWORD_HASH`  | Base64-encoded Argon2 hash for admin panel login    | -                        |
| `JWT_SECRET`           | Secret used to sign admin session JWTs              | -                        |
| `CORS_ORIGINS`         | Allowed CORS origins (JSON list)                    | `["http://localhost:3000"]` |
| `LOG_LVL`              | Log level                                          | `INFO`                   |
| `SHOW_DOCS`            | Enable `/docs` and `/redoc`                         | `true`                   |
| `DB_POOL_SIZE`         | SQLAlchemy connection pool size                     | `10`                     |
| `DB_MAX_OVERFLOW`      | SQLAlchemy pool max overflow                        | `20`                     |

### 2. Run with Docker Compose (recommended)

```bash
docker compose up -d --build
```

This starts a PostgreSQL container and the FastAPI application. Migrations run automatically on startup via `entrypoint.sh`. The API is available at `http://localhost:8000`.

Shortcuts are also available via `Makefile`:

```bash
make reload   # docker compose build && docker compose up -d
make down     # docker compose down
```

### 3. Run locally without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload
```

## API Documentation

Interactive API docs are available (when `SHOW_DOCS=true`):

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Admin Panel

The admin panel is powered by [SQLAdmin](https://aminalaee.dev/sqladmin/) and mounted on the app root. Login requires a JWT secret and an Argon2 password hash configured via `JWT_SECRET` and `ADMIN_PASSWORD_HASH`.

## Database Migrations

Migrations are managed with Alembic:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Code Quality

```bash
make lint   # runs autoflake, isort, and black
```

## Deployment

A GitHub Actions workflow (`.github/workflows/deploy.yml`) is included for manual deployment via SSH, pulling the latest code and rebuilding the Docker Compose stack on the target host.
