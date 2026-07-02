# أثر — Backend API

FastAPI-based REST API for the Athar tourism discovery platform.

## Setup

### Local Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL, API keys, etc.

# Start PostgreSQL with pgvector
docker-compose up -d db redis

# Initialize database + seed data
python -m app.db.seed.seed_data

# Run Alembic migrations (after making model changes)
alembic revision --autogenerate -m "description"
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker-compose up -d
```

## Running Tests

```bash
pip install aiosqlite  # for SQLite in-memory test DB
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Environment Variables

See `.env.example` for all required variables.

Key variables:
- `DATABASE_URL` — PostgreSQL async URL (asyncpg driver)
- `SECRET_KEY` — JWT signing secret (32+ chars)
- `ANTHROPIC_API_KEY` — Claude AI for tourism chat
- `GOOGLE_MAPS_API_KEY` — Maps + Places API
- `COMMISSION_GUIDE=0.20` — 20% platform commission on guide bookings
- `COMMISSION_HOTEL=0.10` — 10% platform commission on hotel bookings

## Architecture

```
app/
├── api/              HTTP layer (routers, middleware, dependencies)
├── core/             Config, security (JWT/bcrypt), logging, exceptions
├── db/               SQLAlchemy base, session, seed data
├── models/           ORM models (User, Spot, Guide, Hotel, Booking, ...)
├── schemas/          Pydantic request/response schemas
├── repositories/     Data access layer (Repository Pattern)
├── services/         Business logic layer
├── utils/            Geo, pagination, Arabic text utilities
├── tasks/            Celery background tasks (AI analysis, emails)
├── ai/               RAG, embeddings, Claude prompts, spot analyzer
└── main.py           FastAPI app factory
```

## Seeded Credentials

- Admin: `admin@athar.sa` / `Admin@2030!`
- Ministry: `ministry@athar.sa` / `Ministry@2030!`
