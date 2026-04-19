# MenuAI

**Snap a photo of any restaurant menu → get every dish translated, described, and labeled with allergens.**

## Why

Living in Istanbul, reading Turkish restaurant menus one line at a time through a
translation app gets old fast. The whole flow — photograph, read, translate dish by
dish, guess the allergens — should collapse into a single action. That's what
MenuAI does.

## Stack

- **Backend** — FastAPI, async SQLAlchemy, PostgreSQL, Alembic, JWT
- **Web** — Next.js 15 (App Router, Server Components), TypeScript, Tailwind
- **Mobile** — Flutter
- **Vision** — Anthropic vision model for menu parsing + dish explanation
- **Infra** — Docker Compose, GitHub Actions

## Repo layout

```
menuai/
├── backend/     FastAPI service (OpenAPI docs at /docs)
├── web/         Next.js frontend
├── mobile/      Flutter app
└── docker-compose.yml
```

## Quick start

```bash
cp .env.example .env
# fill in ANTHROPIC_API_KEY

docker compose up --build
docker compose exec api alembic upgrade head
```

- API → http://localhost:8000 (docs: `/docs`)
- Web → http://localhost:3000

See [`backend/README.md`](./backend/README.md) for the API reference.

## License

MIT
