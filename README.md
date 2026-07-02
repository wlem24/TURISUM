# أثر — Athar 🇸🇦

## اكتشف ما تركه الزمان | Discover what time left behind

An AI-powered tourism discovery platform connecting travelers with undiscovered Saudi Arabia through local knowledge, AI discovery, and verified guides — aligned with **Saudi Vision 2030**.

---

## Project Structure

```
hidden-ksa/
├── frontend/          React 18 + Vite SPA (Arabic/English bilingual, RTL-first)
└── backend/           FastAPI REST API (Python, async, PostgreSQL + pgvector)
```

The frontend and backend are **completely decoupled** — they communicate only via REST API.

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for frontend dev)
- Python 3.12+ (for backend dev)

### 1. Clone & Configure

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit both .env files with your API keys
```

### 2. Start with Docker

```bash
cd backend
docker-compose up -d
```

This starts: PostgreSQL (pgvector), Redis, FastAPI backend, Celery worker.

### 3. Initialize Database

```bash
docker-compose exec backend python -m app.db.seed.seed_data
```

Default credentials seeded:
- Admin: `admin@athar.sa` / `Admin@2030!`
- Ministry: `ministry@athar.sa` / `Ministry@2030!`

### 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

### 5. API Documentation

Available at `http://localhost:8000/docs` (Swagger UI, development only).

---

## Architecture

```
Frontend (React/Vite)        Backend (FastAPI)
        │                           │
        │──── REST API calls ───────│
        │                           │
        │              ┌────────────┼────────────┐
        │              │            │            │
        │           PostgreSQL   Redis        Celery
        │           + pgvector  (cache/queue)  Workers
        │                           │
        │                    Anthropic Claude API
        │                    OpenStreetMap tiles
        │                    Cloudinary (images)
        │                    Moyasar (payments)
```

### Backend Layers
1. **Routers** — HTTP endpoints (no business logic)
2. **Services** — Business logic (all rules live here)
3. **Repositories** — Data access (SQL queries isolated)
4. **Models** — SQLAlchemy ORM
5. **Schemas** — Pydantic validation

---

## User Roles

| Role | Permissions |
|------|------------|
| `visitor` | Browse spots, book guides/hotels, write reviews |
| `local` | All visitor + submit spots for review |
| `guide` | All visitor + manage profile + view bookings |
| `admin` | All + approve/reject spots + manage users |
| `ministry` | All admin + analytics + bulk spot import |

---

## Commission Model

| Booking Type | Platform Takes | Provider Gets |
|-------------|---------------|---------------|
| Guide booking | 20% | 80% |
| Hotel booking | 10% | 90% |
| Package | blended | blended |

All amounts calculated with `Decimal` precision (never float).

---

## AI Features

1. **AI Discovery Chat** — Claude claude-sonnet-4-6 bilingual tourism assistant
2. **Smart Spot Suggestions (RAG)** — pgvector + sentence-transformers similarity search
3. **Spot Quality Analyzer** — AI evaluates submitted spots before admin review
4. **Interactive Map** — Leaflet + OpenStreetMap pins for approved spots (no API key required)

---

## Spot Approval Workflow

```
Local submits spot (status: pending)
        ↓
AI Analyzer scores & flags issues
        ↓
Admin reviews in PendingSpots dashboard
        ↓
    Approve → spot goes live + submitter notified
    Reject  → reason sent to submitter
```

---

## Tech Stack

**Frontend:** React 18, Vite, Axios, Zustand, React Query, Leaflet (OpenStreetMap), i18next (AR/EN RTL), React Hook Form + Zod, Tailwind CSS

**Backend:** FastAPI, PostgreSQL + pgvector, SQLAlchemy 2.0 async, Alembic, JWT auth, Celery + Redis, Cloudinary, Moyasar

**AI/RAG:** Anthropic Claude claude-sonnet-4-6, sentence-transformers (multilingual), pgvector

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login → access + refresh token |
| POST | `/api/v1/auth/refresh` | Rotate refresh token |
| GET | `/api/v1/spots` | List approved spots (paginated, filtered) |
| POST | `/api/v1/spots` | Submit spot (local+) |
| POST | `/api/v1/spots/{id}/approve` | Approve/reject (admin+) |
| GET | `/api/v1/guides` | List available guides |
| GET | `/api/v1/hotels` | List hotels |
| GET | `/api/v1/hotels/nearby` | Hotels near coordinates |
| POST | `/api/v1/bookings` | Create booking with commission |
| GET | `/api/v1/regions` | All 13 Saudi regions |
| GET | `/api/v1/admin/dashboard` | Platform stats (admin+) |
| POST | `/api/v1/ai/chat` | AI tourism chat |
| POST | `/api/v1/ai/suggest` | RAG spot suggestions |

---

## Vision 2030 Alignment

- Promotes domestic tourism and undiscovered Saudi destinations
- Empowers local communities through the spot submission system
- Creates income opportunities for certified local guides
- Bilingual Arabic-first interface respecting cultural identity
- Supports the tourism sector's goal of 150M visitors by 2030

---

*Built with ❤️ for Saudi Arabia 🇸🇦*
