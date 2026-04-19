# MenuAI — Web

Next.js 15 (App Router) frontend for MenuAI. Talks to the FastAPI backend.

## Stack

- Next.js 15 + React 19
- TypeScript (strict)
- Tailwind CSS
- Server Actions for mutations, httpOnly-cookie session for auth
- Middleware guard on `/app/*`

## Layout

```
src/
├── app/
│   ├── layout.tsx           root
│   ├── page.tsx             landing
│   ├── (auth)/              login + register (shared layout + actions)
│   └── app/                 authenticated area (nav, history, scan, favorites)
├── components/              DishCard, ScanForm, AuthForm, FavoriteButton
├── lib/
│   ├── api.ts               typed ApiClient
│   ├── session.ts           cookie-backed session helpers
│   └── languages.ts
└── middleware.ts            redirects unauthenticated traffic off /app
```

## Run

```bash
cp .env.example .env.local
# make sure the backend is running (see ../backend/README.md)

npm install
npm run dev
```

Web → http://localhost:3000
