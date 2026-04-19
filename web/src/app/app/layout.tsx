import Link from "next/link";
import { redirect } from "next/navigation";

import { logoutAction } from "@/app/(auth)/actions";
import { getCurrentUser } from "@/lib/session";

export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const user = await getCurrentUser();
  if (!user) redirect("/login");

  return (
    <div className="min-h-screen bg-ink-50">
      <header className="border-b border-ink-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Link href="/app" className="font-display text-xl font-semibold">
            MenuAI
          </Link>
          <nav className="flex items-center gap-1 text-sm">
            <NavLink href="/app/scan">Scan</NavLink>
            <NavLink href="/app/import">Import URL</NavLink>
            <NavLink href="/app">History</NavLink>
            <NavLink href="/app/favorites">Favorites</NavLink>
            <form action={logoutAction}>
              <button type="submit" className="btn-ghost ml-2 text-sm">
                Log out
              </button>
            </form>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
    </div>
  );
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href} className="rounded-md px-3 py-1.5 text-ink-700 hover:bg-ink-100">
      {children}
    </Link>
  );
}
