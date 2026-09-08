# Subby — Agent Guide

## Learning and collaboration goals

- Act as an advisor who helps the user improve their backend development skills.
- Always use simple technical English. Explain unfamiliar terms briefly.
- Focus on completing a deployable backend API before doing more frontend work.
- Break work into small, enjoyable tasks that can usually be finished in one
  short learning session.
- Explain why a change is useful before or while guiding its implementation.
- Prefer guided practice: give the user a chance to implement important parts,
  then review their work and offer clear feedback.
- Make progress visible. Each task should end with a useful result, such as a
  working endpoint, passing check, migration, or deployment improvement.
- Introduce only a small number of new concepts in each task and connect them
  to code that already exists in this repository.
- Keep the backend learning path focused on API design, validation, database
  operations, testing, configuration, security, Docker, and deployment.

## Repository overview

Subby is a Docker-orchestrated subscription tracker with a React single-page
frontend and a FastAPI REST backend. PostgreSQL persists data; Alembic owns its
schema migrations. Nginx is the public reverse proxy.

```
.
├── docker-compose.yml       # Runs PostgreSQL, backend, frontend, and Nginx
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI router hierarchy and HTTP endpoints
│   │   ├── db/              # SQLAlchemy engine, session dependency, Base
│   │   ├── models/          # SQLAlchemy Subscription, Installment, Payment models/enums
│   │   ├── schema/          # Pydantic request/response types
│   │   ├── services/        # Database/domain operations
│   │   ├── exceptions.py    # DomainException mapped to HTTP 400
│   │   └── main.py          # FastAPI app; external root path is /api
│   ├── alembic/             # Migration environment and revision files
│   ├── pyproject.toml       # Python dependency declarations
│   ├── uv.lock              # Locked Python dependency graph; commit updates
│   ├── Dockerfile
│   └── entrypoint.sh        # Applies migrations before starting Uvicorn
├── frontend/
│   ├── src/                 # React app, styles, and imported assets
│   ├── public/              # Static files
│   ├── package.json         # npm scripts and JS dependencies
│   ├── package-lock.json    # Locked npm dependencies; commit updates
│   ├── vite.config.ts
│   └── Dockerfile
└── nginx/nginx.conf         # /api/ → backend, all other traffic → Vite
```

## Tech stack and dependencies

- **Backend:** Python 3.12+, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic
  (through FastAPI), Alembic, and `psycopg2-binary`.
- **Python environment/package manager:** `uv`; `backend/uv.lock` is the source
  of reproducible installed versions. The backend Docker image uses `uv sync
  --frozen`.
- **Database:** PostgreSQL 18 in Docker Compose. The default Compose database is
  `postgresql://user:password@db:5432/subbydb`.
- **Frontend:** React 19, TypeScript 6, Vite 8, and ESLint 10. Development uses
  npm and the committed `package-lock.json`.
- **Deployment/development proxy:** Nginx forwards `/api/` to FastAPI and other
  paths to Vite. Compose exposes Nginx on `http://localhost:8000`.

## Backend architecture

- Define persistence models in `backend/app/models/`; export new models from
  `models/__init__.py` so Alembic's `import app.models` registers their metadata.
- Put API validation and serialized outputs in `backend/app/schema/`.
- Keep endpoint modules thin: use `backend/app/services/` for database logic and
  inject a SQLAlchemy `Session` through `get_db`.
- Routes are versioned under `/api/v1`. Current endpoints are:
  - `GET /api/health/`
  - `GET /api/v1/subscriptions/` (paginated; `page`, `size`)
  - `GET /api/v1/subscriptions/{subscription_id}`
  - `POST /api/v1/subscriptions/`
- Raise `DomainException` for expected domain failures; `main.py` renders it as
  a 400 JSON response. Use `HTTPException` for endpoint-level HTTP errors.

## Core commands

Run these from the repository root unless a command starts with `cd`.

### Full stack (recommended)

```sh
docker compose up --build
docker compose down
docker compose logs -f backend
```

The backend container runs `alembic upgrade head` automatically at startup.
Nginx serves the stack at `http://localhost:8000`; API requests go through
`http://localhost:8000/api/`.

### Backend local development

```sh
cd backend
uv sync
DATABASE_URL='postgresql://user:password@localhost:5432/subbydb' \
  uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Start PostgreSQL first with `docker compose up -d db` when using the default
local connection string. Apply or inspect migrations manually with:

```sh
cd backend
DATABASE_URL='postgresql://user:password@localhost:5432/subbydb' \
  uv run alembic upgrade head
DATABASE_URL='postgresql://user:password@localhost:5432/subbydb' \
  uv run alembic revision --autogenerate -m 'describe change'
DATABASE_URL='postgresql://user:password@localhost:5432/subbydb' \
  uv run alembic current
```

Review autogenerated migrations before committing them. Do not hand-edit the
lockfile; use `uv` when changing Python dependencies.

### Frontend development and checks

```sh
cd frontend
npm install
npm run dev
npm run build
npm run lint
npm run preview
```

`npm run build` runs TypeScript project builds before producing `dist/`. There
is no configured frontend test command and no backend test suite/configuration
at present; use the build and lint commands as the available checks.

## Working conventions

- Preserve the lockfiles (`backend/uv.lock`, `frontend/package-lock.json`) when
  changing dependencies, and commit their intentional updates alongside manifest
  changes.
- Never commit local environments, `node_modules`, `.env*` secrets, build output,
  or Python cache files; the existing `.gitignore` files cover these.
- Backend configuration currently comes from `DATABASE_URL`; keep secrets out of
  source and use environment variables for new configuration.
- Keep the Nginx `/api/` prefix and FastAPI `root_path="/api"` aligned when
  changing routing or deployment behavior.
- The frontend currently has no API client abstraction. Add one deliberately
  rather than scattering fetch calls across UI components.
