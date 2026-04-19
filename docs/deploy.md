# Deploy

Two services, two providers. Backend on Railway (gives us PostgreSQL + Redis for
free), web on Vercel (Next.js is its first-class workload).

---

## 1 · Backend on Railway

### Create the project

1. https://railway.app → New Project → **Deploy from GitHub repo** → pick `menuai`
2. Set **Root Directory** to `backend`
3. Railway auto-detects the Dockerfile

### Add a PostgreSQL plugin

1. In the project: **+ New** → **Database** → **PostgreSQL**
2. Railway creates a managed Postgres and injects `DATABASE_URL`
3. Override the DB URL so async drivers work:
   - In the API service → **Variables** → add:
     ```
     DATABASE_URL=postgresql+asyncpg://${{Postgres.PGUSER}}:${{Postgres.PGPASSWORD}}@${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}
     ```

### Add a Redis plugin

1. **+ New** → **Database** → **Redis**
2. Railway injects `REDIS_URL` automatically.

### API service environment

| Variable             | Value                                          |
|----------------------|------------------------------------------------|
| `ANTHROPIC_API_KEY`  | your key                                       |
| `JWT_SECRET`         | run `openssl rand -hex 32` and paste the output|
| `CORS_ORIGINS`       | your deployed web URL, e.g. `https://menuai-web.vercel.app` |

### Run migrations

Once deployed, open Railway's shell for the API service and run:

```bash
alembic upgrade head
```

### Expose a public URL

API service → **Settings** → **Networking** → **Generate Domain**. Note the URL —
Vercel will need it.

---

## 2 · Web on Vercel

### Import the repo

1. https://vercel.com/new → import `menuai`
2. Set **Root Directory** to `web`
3. Vercel auto-detects Next.js — leave Build Command and Output as defaults

### Environment variables

| Variable                     | Value                                |
|------------------------------|--------------------------------------|
| `API_BASE_URL`               | Railway API URL (e.g. `https://menuai-api.up.railway.app`) |
| `NEXT_PUBLIC_API_BASE_URL`   | same value                           |

Add them to **Production**, **Preview**, and **Development** so PR previews work.

Deploy. Vercel gives you `https://<project>.vercel.app`.

### Fix CORS

Go back to Railway → API service → **Variables** → update `CORS_ORIGINS` to the
Vercel URL. Redeploy the API so the change takes effect.

---

## 3 · Mobile

Mobile doesn't deploy to anything — it gets built and shipped to TestFlight /
Play Console.

For a quick demo build:

```bash
cd mobile
flutter build ios --release --dart-define=API_BASE_URL=https://menuai-api.up.railway.app
flutter build apk --release --dart-define=API_BASE_URL=https://menuai-api.up.railway.app
```

`build/ios/iphoneos/Runner.app` and `build/app/outputs/flutter-apk/app-release.apk`
can be side-loaded for the interview demo if needed.

---

## 4 · Smoke test after deploying

```bash
API=https://menuai-api.up.railway.app

curl $API/health
# {"status":"ok"}

curl -X POST $API/auth/register \
  -H "content-type: application/json" \
  -d '{"email":"demo@example.com","password":"supersecret","target_language":"en"}'
# {"access_token":"..."}
```

If `/health` returns 200 and `/auth/register` returns a token, you're in. Open
the Vercel URL, register, scan a menu photo.

---

## Rollback

Railway and Vercel both keep the last N deploys. If a deploy misbehaves:

- **Vercel**: Deployments → find the previous one → **Promote to Production**
- **Railway**: Deployments → find the previous one → **Redeploy**

Never force-push to `main` to "undo" a deploy — use the platform's rollback
instead, then fix forward.
