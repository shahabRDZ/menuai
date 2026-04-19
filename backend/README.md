# MenuAI — Backend

FastAPI backend for MenuAI. Takes a menu photo, returns a structured list of dishes
with translation, ingredients, and allergen info.

## Stack

- FastAPI (async)
- PostgreSQL via SQLAlchemy 2 async + Alembic
- Redis (caching, ready to use)
- JWT auth (HS256) + bcrypt password hashing
- Anthropic vision model for menu parsing

## Architecture

Clean layered layout:

- `models/`       SQLAlchemy ORM
- `schemas/`      Pydantic request/response contracts
- `repositories/` Data access (generic `BaseRepository[T]` + concrete subclasses)
- `services/`     Business logic (`AuthService`, `MenuService`, `FavoriteService`,
                  `MenuVisionService`, `PasswordHasher`, `TokenService`)
- `routers/`      Thin HTTP handlers, wired through FastAPI's dependency system
- `exceptions.py` Domain errors subclassed from `HTTPException`

## Run with Docker (from repo root)

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY

docker compose up --build
```

Apply migrations (first run only):

```bash
docker compose exec api alembic upgrade head
```

API is live at http://localhost:8000 — interactive docs at `/docs`.

## Run locally without Docker

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# run postgres + redis separately (or `docker compose up postgres redis`)
export DATABASE_URL="postgresql+asyncpg://menuai:menuai_dev@localhost:5432/menuai"
export ANTHROPIC_API_KEY="sk-ant-..."

alembic upgrade head
uvicorn app.main:app --reload
```

## Endpoints

| Method | Path                  | Purpose                                          |
|--------|-----------------------|--------------------------------------------------|
| POST   | `/auth/register`      | Create user, return JWT                          |
| POST   | `/auth/login`         | Login (OAuth2 form), return JWT                  |
| GET    | `/auth/me`            | Current user profile                             |
| POST   | `/menus/scan`         | **Upload menu photo → AI-parsed dish list**      |
| GET    | `/menus`              | List user's previous scans                       |
| GET    | `/menus/{id}`         | Full scan with dishes                            |
| DELETE | `/menus/{id}`         | Delete a scan                                    |
| POST   | `/menus/explain`      | Explain a single dish name (no photo)            |
| POST   | `/favorites/{dish_id}`| Save a dish as favorite                          |
| DELETE | `/favorites/{dish_id}`| Remove a favorite                                |
| GET    | `/favorites`          | List favorite dishes                             |
| GET    | `/health`             | Health check                                     |

## Example: scan a menu

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "content-type: application/json" \
  -d '{"email":"you@example.com","password":"supersecret","target_language":"en"}'
# → {"access_token": "..."}

# 2. Scan a menu photo
TOKEN="..."
curl -X POST http://localhost:8000/menus/scan \
  -H "authorization: Bearer $TOKEN" \
  -F "image=@menu.jpg" \
  -F "target_language=en"
```

## Tests

```bash
cd backend
pytest
```

## Prompt caching

Both vision system prompts are marked with `cache_control: ephemeral`, so repeat
requests only bill for the image + user turn. This matters when a user scans
several menu photos in a row.
