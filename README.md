# Fantasy Analyzer

A dynasty fantasy football trade analyzer and league power-ranking tool, built as a full-stack portfolio project demonstrating backend API design, cloud deployment, and a custom valuation algorithm.

Import a real Sleeper league, get instant power rankings with per-position breakdowns, and evaluate trades using a hand-tuned dynasty valuation model — all served through a self-hosted API running on AWS.

## Tech Stack

**Backend:** FastAPI, SQLModel, PostgreSQL, Alembic, Docker
**Frontend:** React, TypeScript, Vite, React Router, React Context
**Auth:** Google OAuth (`@react-oauth/google` + server-side token verification + JWT sessions)
**Data sources:** [Sleeper API](https://docs.sleeper.com/) (players, leagues, rosters, draft picks), [nflreadpy](https://github.com/nflverse/nflreadpy) (season stats, draft capital crosswalk)
**Infrastructure:** AWS EC2 (Dockerized backend), AWS RDS (PostgreSQL)

## Features

### Dynasty Valuation Engine
A custom algorithm (`valuation.py`) that scores every player on a normalized 0–10,000 scale, combining:
- Position-specific age curves (peak windows and decay rates tuned per position — RBs decline fast, QBs age gracefully)
- Replacement-level production baselines, computed separately for 1QB and Superflex formats
- Positional scarcity multipliers that shift dramatically between formats (QB value roughly doubles in Superflex)
- A draft-capital fallback for unproven rookies with no NFL production yet, tiered by pick slot

### Trade Calculator
Search-and-select UI for building both sides of a trade, live running point totals per side, a 1QB/Superflex toggle, and a fairness verdict computed server-side against real player values.

### League Import & Power Rankings
Paste a Sleeper league ID to import real rosters, records, and team ownership. Produces a ranked leaderboard with:
- Total roster value, record, and average age per team
- Per-position value and league-wide rank, color-coded by tier
- Expandable rows showing every player on a roster grouped by position

### Google Sign-In
Save imported leagues to your account and revisit them without re-entering a league ID.

## Data Pipeline

Player biographical data is pulled from Sleeper's public players endpoint. Season stats and NFL draft capital come from `nflreadpy` (the actively maintained successor to the now-archived `nfl_data_py`), matched back to Sleeper's player IDs via a cross-platform ID crosswalk table. Both sources are upserted, not duplicated, on every sync.

```
sync_players.py    → pulls player roster/bio data from Sleeper
sync_stats.py      → pulls season stats + draft capital from nflreadpy, matches via crosswalk
run_valuation.py   → runs the valuation pipeline, writes results to PlayerValue
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/players` | List players, filterable by position, sorted by value |
| GET | `/players/{id}` | Single player detail |
| POST | `/trade/evaluate` | Evaluate a proposed trade between two sides |
| POST | `/leagues/import` | Import a Sleeper league by ID |
| GET | `/leagues/{id}/rankings` | Full power-ranking breakdown for an imported league |
| POST | `/auth/google` | Exchange a Google ID token for an app session token |
| GET | `/users/me/leagues` | List leagues saved to the current account |

Interactive docs available at `/docs` when running locally.

## Data Model

`Player`, `PlayerSeason`, `PlayerValue`, `League`, `Team`, `RosterSlot`, `DraftPick`, `User`, `UserLeague` — all managed through SQLModel with Alembic migrations for schema versioning.

## Running Locally

**Prerequisites:** Python 3.13, Node.js, Docker Desktop, a Google OAuth Client ID.

**1. Database**
```bash
docker start dynasty-db
```

**2. Backend** (`backend/app/`)
```bash
venv\Scripts\Activate.ps1
uvicorn main:app --reload
```
Requires a `backend/.env` with `DATABASE_URL`, `JWT_SECRET`, and `GOOGLE_CLIENT_ID`.

**3. Frontend** (`frontend/`)
```bash
npm run dev
```
Requires a `frontend/.env` with `VITE_GOOGLE_CLIENT_ID` and `VITE_API_BASE`.

Visit `http://localhost:5173`.

## Deployment

The backend is Dockerized and deployed to an EC2 instance (Amazon Linux 2023), connected to a PostgreSQL instance on RDS. The database has no public access — inbound traffic is restricted at the security-group level to the EC2 instance alone. Schema migrations run against RDS via `alembic upgrade head` inside the running container.

The frontend is not yet deployed to a public host; it currently runs via local Vite dev server only.

## Known Limitations

- Draft pick capital is not yet factored into league power rankings (roster value only)
- Frontend has no production deployment yet (planned: AWS Amplify)
- No custom domain or HTTPS on the backend yet
- Minimal visual styling — functionality-first, a full design pass is still outstanding
- `PlayerValue` intentionally retains history across recomputations rather than overwriting, so values reflect the most recent run per player/format

## Project Structure

```
backend/
  app/
    main.py           # FastAPI app entrypoint
    database.py        # engine + session management
    models.py           # SQLModel table definitions
    schemas.py           # Pydantic request/response schemas
    valuation.py          # dynasty valuation algorithm
    auth.py                 # Google token verification + JWT
    routers/                  # players, leagues, auth route modules
  alembic/                      # schema migrations
  Dockerfile
frontend/
  src/
    pages/               # App (players), TradeCalculator, LeagueImport
    components/            # PlayerSearch, Nav, LoadingSpinner
    api/                      # typed fetch wrappers
    context/                    # AuthContext (React Context)
    types/                        # shared TypeScript interfaces
```