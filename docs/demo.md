# MenuAI — 5-minute demo script

A walkthrough for showing MenuAI to someone who has never seen it. Designed for
technical interviews: heavy on what's happening under the hood, light on
marketing talk.

---

## 0 · Before the meeting (1 min of prep)

- Start the stack: `docker compose up -d && docker compose exec api alembic upgrade head`
- Start the web: `cd web && npm run dev`
- Have **one Turkish menu photo** saved to the desktop for the scan demo
- Open three tabs:
  1. http://localhost:3000
  2. http://localhost:8000/docs
  3. https://github.com/shahabRDZ/menuai

---

## 1 · The problem (30 sec)

> I live in Istanbul. Every time I sit down at a new restaurant I end up taking a
> photo of the menu and translating it word by word in another app. That whole
> flow should collapse into one action: point the camera, read the menu like a
> local. That's MenuAI.

Keep this short — the interviewer doesn't need convincing the problem is real.

---

## 2 · The product (1 min — demo on the web app)

1. Open http://localhost:3000 — landing page
2. Click **Register**, create an account, choose **Persian** or **English** as
   target language
3. Click **Scan** — drop in the Turkish menu photo
4. While it loads (3–5 seconds), narrate what's happening:
   > "This image goes to FastAPI, we compress it, send it to the vision model
   > with a cached system prompt, and get back a structured list of dishes.
   > The whole page you're about to see is the model's JSON turned into
   > typed Pydantic objects."
5. Scan detail page appears. Point at:
   - Translated name + original name side by side
   - Description (not in the original menu — generated)
   - Tags: category, vegetarian, spice level, allergens
   - Ingredients line at the bottom
6. Star one dish → go to **Favorites** tab → it's there

**Keep this part under a minute. The demo sells itself.**

---

## 3 · The code (2 min)

Pull up the repo. Walk through, briefly:

### Backend layout

```
backend/app/
├── models/        SQLAlchemy ORM
├── schemas/       Pydantic contracts
├── repositories/  Generic BaseRepository[T] + concrete subclasses
├── services/      AuthService, MenuService, FavoriteService,
                   MenuVisionService, PasswordHasher, TokenService
├── routers/       Thin HTTP handlers, dependencies injected via FastAPI DI
└── exceptions.py  Domain errors subclassed from HTTPException
```

> "The interesting decision is the repository/service split. Routers only know
> HTTP. Services only know business logic. Repositories only know SQLAlchemy.
> I can swap the database or swap the model provider without touching the
> other layers."

Open `app/repositories/base.py`:

> "Generic `BaseRepository[T]` so concrete repositories don't re-implement
> `get`, `add`, `delete`. Inheritance earning its keep."

Open `app/services/ai.py`:

> "One class per external system. The vision service has two methods —
> `scan_menu` and `explain_dish`. Both use ephemeral prompt caching on
> the stable system prompts, so repeat calls only pay for the user turn.
> That matters when a user scans three photos in a row."

### Web layout

Open `web/src/app/app/scan/actions.ts`:

> "Every mutation is a Server Action. The token lives in an httpOnly cookie,
> never touches the client. Middleware guards `/app/*`. There's no state
> management library — Server Actions plus `revalidatePath` cover the whole
> app."

### Mobile layout

Open `mobile/lib/features/scans/scans_controller.dart`:

> "Each feature has a `ChangeNotifier` controller. Optimistic UI on favorite
> toggles: update the local state, roll back if the API call fails. The
> `ApiClient` is injected through `Provider` so every controller is trivial
> to test."

---

## 4 · AI in the workflow (1 min)

> "This was built in four days by orchestrating Claude Code agents. I ran
> specialized sub-agents in parallel: one explored the repository, another
> scaffolded the Next.js code while I was finishing the FastAPI layer,
> and a review agent audited each change in a separate context before commit."

If they ask for specifics:

- Sub-agents (Explore, Plan, review, security-review) run in isolated contexts
- Hooks in `settings.json` run tests after every edit
- Skills wrap repetitive flows (e.g. `/security-review`) so the team can share them
- Memory in `.claude/projects/…/memory/` persists user + project context across sessions

> "The productivity win is real — I estimate 3–5× vs editing alone — but the
> bigger win is that I stay in architect mode. I review every diff."

---

## 5 · Their likely follow-up questions (prepared)

**Q: What happens if the vision model returns bad JSON?**
> `MenuVisionService._parse_json_response` handles fenced code blocks and raises
> `UpstreamError` (502) on bad JSON. The scan endpoint surfaces that directly to
> the client. In production I'd add a retry with a nudge prompt.

**Q: How do you prevent image abuse / cost abuse?**
> Three layers: auth-gated endpoint, 10 MB size cap, image compression to 1600px
> max before sending to the model. Next step is per-user rate limiting in Redis
> (the dependency is already wired up).

**Q: How would you scale this?**
> Backend is already stateless and horizontally scalable behind ALB/Fargate.
> Postgres fronted by PgBouncer. The only place I'd change things is moving
> vision calls to a background worker (e.g. RQ / Celery) so the HTTP request
> returns immediately and the client polls for the scan result.

**Q: Why not use an ORM abstraction you wrote yourself?**
> SQLAlchemy already gives us what we need. The repository layer is thin on
> purpose — it's there so routes don't talk to the session directly, not to
> replace SQLAlchemy.

**Q: Why Flutter and not native?**
> Shipping speed. MenuAI's UX is a few forms and a list view — Flutter nails
> both platforms with one codebase. If the app grew into heavy camera
> processing or AR, I'd write the performance-critical parts in Swift and
> Kotlin and bridge.

---

## 6 · Close (30 sec)

> "Four-day project, three platforms, full CI, AI in the build process and in
> the product. If there's anything you'd like to see at a different level of
> depth — data modeling, the vision prompts, the Next.js Server Actions wiring,
> the Flutter state — happy to dig in."

Then: **stop talking**. Let them drive.
