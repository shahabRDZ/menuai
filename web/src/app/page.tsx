import Link from "next/link";

import { getCurrentUser } from "@/lib/session";

export default async function LandingPage() {
  const user = await getCurrentUser();

  return (
    <main className="min-h-screen">
      <header className="border-b border-ink-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Link href="/" className="font-display text-xl font-semibold text-ink-900">
            MenuAI
          </Link>
          <nav className="flex items-center gap-2 text-sm">
            {user ? (
              <Link href="/app" className="btn-primary">
                Open app
              </Link>
            ) : (
              <>
                <Link href="/login" className="btn-ghost">
                  Log in
                </Link>
                <Link href="/register" className="btn-primary">
                  Get started
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      <section className="mx-auto max-w-5xl px-6 py-20">
        <div className="grid gap-12 md:grid-cols-2 md:items-center">
          <div>
            <p className="mb-3 text-sm font-semibold uppercase tracking-wide text-accent-600">
              Never guess at a menu again
            </p>
            <h1 className="font-display text-5xl font-semibold leading-tight text-ink-900">
              Point your camera. <br /> Read the menu like a local.
            </h1>
            <p className="mt-5 max-w-prose text-lg text-ink-700">
              Snap a photo of any restaurant menu and MenuAI returns every dish translated,
              described, and tagged with likely allergens — in seconds.
            </p>
            <div className="mt-8 flex items-center gap-3">
              <Link href={user ? "/app/scan" : "/register"} className="btn-primary">
                {user ? "Scan a menu" : "Try it free"}
              </Link>
              <Link href="/login" className="btn-ghost">
                I already have an account
              </Link>
            </div>
          </div>

          <div className="card p-6">
            <ul className="space-y-4 text-sm text-ink-700">
              <Feature
                title="Any language in, your language out"
                body="Turkish, Arabic, Japanese, Italian — if the camera can read it, MenuAI can translate it."
              />
              <Feature
                title="Ingredients and allergens"
                body="Each dish comes back with likely ingredients and common allergen flags (gluten, dairy, nuts, seafood…)."
              />
              <Feature
                title="Save what you love"
                body="Tap a star to keep favorite dishes around across restaurants and trips."
              />
              <Feature
                title="Works on your phone"
                body="Capture on mobile, review on the web dashboard, export anywhere."
              />
            </ul>
          </div>
        </div>
      </section>

      <footer className="border-t border-ink-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-6 text-sm text-ink-500">
          <p>© {new Date().getFullYear()} MenuAI</p>
          <a
            href="https://github.com/shahabRDZ/menuai"
            className="hover:text-ink-900"
            rel="noreferrer"
            target="_blank"
          >
            Source on GitHub
          </a>
        </div>
      </footer>
    </main>
  );
}

function Feature({ title, body }: { title: string; body: string }) {
  return (
    <li>
      <p className="font-medium text-ink-900">{title}</p>
      <p className="mt-1">{body}</p>
    </li>
  );
}
