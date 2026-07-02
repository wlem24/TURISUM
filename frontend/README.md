# أثر — Frontend

React 18 + Vite SPA for the Athar tourism discovery platform.

## Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your API URL
npm run dev
# Opens at http://localhost:5173
```

## Build for Production

```bash
npm run build
# Output in dist/
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Backend API URL (default: `http://localhost:8000/api/v1`) |
| `VITE_APP_NAME` | App name (default: `أثر`) |
| `VITE_DEFAULT_LANG` | Default language: `ar` or `en` |

## Tech Stack

- **React 18** + **Vite** — Fast SPA
- **Axios** — HTTP client with JWT auto-attach + refresh interceptor
- **React Router v6** — Client-side routing
- **Zustand** — Global state (auth, spots, UI)
- **React Query** — Server state + caching
- **Leaflet + react-leaflet** — Interactive maps via OpenStreetMap (no API key)
- **i18next** — Arabic/English bilingual with RTL support
- **React Hook Form + Zod** — Form validation
- **Tailwind CSS + tailwindcss-rtl** — Styling with RTL support
- **react-hot-toast** — Toast notifications

## RTL Support

The app is Arabic-first (RTL). Switch with the language toggle in the navbar.

The HTML `dir` and `lang` attributes are set dynamically. All Tailwind CSS uses logical properties (`start`/`end` instead of `left`/`right`) for RTL compatibility.

## Pages

| Route | Description | Auth Required |
|-------|-------------|---------------|
| `/explore` | Browse all approved spots | No |
| `/spots/:id` | Spot detail page | No |
| `/guides` | List tour guides | No |
| `/hotels` | List hotels | No |
| `/ai-explorer` | AI tourism chat | Yes |
| `/submit-spot` | Submit a new spot | Local+ |
| `/profile` | User profile + bookings | Yes |
| `/admin` | Admin dashboard | Admin+ |
| `/admin/pending-spots` | Review pending spots | Admin+ |
