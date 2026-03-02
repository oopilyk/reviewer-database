# Reviewer Database / Reviewer API Service

Standalone Django app that exposes a **REST API for reviewer data**. It can use the **same database** as SUPERGOODI (read/write the same `reviewers_reviewer` tables) or run with its own SQLite DB.

## Setup

```bash
cd reviewer-database
python -m venv venv
source venv/bin/activate   # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Use SUPERGOODI's database (shared)

Point the service at SUPERGOODI's SQLite file so both apps see the same reviewers:

```bash
export DB_PATH=/path/to/SUPERGOODI/supergoodi/db.sqlite3
python manage.py runserver 8001
```

Example if SUPERGOODI is in a sibling directory:

```bash
export DB_PATH=../SUPERGOODI/supergoodi/db.sqlite3
python manage.py runserver 8001
```

## Use own database (empty)

If you don't set `DB_PATH`, the app uses `db.sqlite3` in this directory. The models are **managed=False** (they don't create tables), so this only works if you run against an existing DB (e.g. SUPERGOODI's) or add migrations later for a standalone schema.

## API

Base URL: `http://localhost:8001/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reviewers/` | List reviewers (paginated). Query params: `panel_id`, `mission`, `cycle`, `status`, `search`, `ordering` |
| POST | `/api/reviewers/` | Create reviewer |
| GET | `/api/reviewers/{id}/` | Get one reviewer |
| PUT/PATCH | `/api/reviewers/{id}/` | Update reviewer |
| DELETE | `/api/reviewers/{id}/` | Delete reviewer |
| GET | `/api/reviewers/{id}/conflicts/` | Get conflict proposal IDs (PI, CoI, inst, collab, other, target) |
| GET | `/api/reviewers/{id}/proposals/` | Get assigned proposal IDs (primary, secondary) |

### Query parameters (list)

- `panel_id` – filter by panel
- `mission` – e.g. `nustar`, `fermi`, `ixpe`
- `cycle` – e.g. `12`
- `status` – e.g. `Y`, `U`
- `search` – search in fname, lname, email, inst
- `ordering` – e.g. `lname`, `-fname`

### Example

```bash
# List reviewers for NuSTAR cycle 12
curl "http://localhost:8001/api/reviewers/?mission=nustar&cycle=12"

# Get one reviewer
curl "http://localhost:8001/api/reviewers/1/"
```

## CORS

When SUPERGOODI (e.g. on port 8000) calls this API (e.g. on 8001), the browser may block cross-origin requests. This project uses `django-cors-headers`. In development, `DEBUG=True` allows all origins. For production, set `CORS_ALLOWED_ORIGINS` or the env var `CORS_ORIGINS` (comma-separated).

## Connecting SUPERGOODI to this API

In SUPERGOODI's settings (or env):

- `REVIEWER_SERVICE_USE_API=True`
- `REVIEWER_SERVICE_URL=http://localhost:8001` (or the URL of this service)

Then implement `ReviewerAPIClient` in SUPERGOODI's `reviewers/api_client.py` to call these endpoints and plug it into `ReviewerClient` when `use_api=True`.
