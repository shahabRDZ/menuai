import Link from "next/link";

import { api } from "@/lib/api";
import { languageLabel } from "@/lib/languages";
import { requireSession } from "@/lib/session";

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default async function HistoryPage() {
  const { token } = await requireSession();
  const scans = await api.listScans(token);

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl font-semibold">Your scans</h1>
          <p className="mt-1 text-sm text-ink-500">
            {scans.length === 0
              ? "No scans yet. Point your camera at a menu to get started."
              : `${scans.length} scan${scans.length === 1 ? "" : "s"} saved.`}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/app/import" className="btn-ghost">
            Import URL
          </Link>
          <Link href="/app/scan" className="btn-primary">
            New scan
          </Link>
        </div>
      </header>

      {scans.length === 0 ? (
        <EmptyState />
      ) : (
        <ul className="grid gap-3 sm:grid-cols-2">
          {scans.map((scan) => (
            <li key={scan.id}>
              <Link
                href={`/app/scans/${scan.id}`}
                className="card block p-5 transition hover:border-accent-500"
              >
                <p className="font-medium text-ink-900">
                  {scan.restaurant_name ?? "Untitled menu"}
                </p>
                <p className="mt-1 text-sm text-ink-500">
                  {scan.dish_count} {scan.dish_count === 1 ? "dish" : "dishes"} ·{" "}
                  {languageLabel(scan.target_language)} · {formatDate(scan.created_at)}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function EmptyState() {
  return (
    <div className="card flex flex-col items-center p-12 text-center">
      <p className="font-display text-lg font-semibold">Nothing here yet</p>
      <p className="mt-2 max-w-sm text-sm text-ink-500">
        Your scan history will appear here. Each scan keeps every dish translated and tagged so
        you can come back to it anytime.
      </p>
      <Link href="/app/scan" className="btn-primary mt-6">
        Scan your first menu
      </Link>
    </div>
  );
}
