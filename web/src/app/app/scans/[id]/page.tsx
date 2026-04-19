import Link from "next/link";
import { notFound } from "next/navigation";

import { DishCard } from "@/components/dish-card";
import { api, ApiError } from "@/lib/api";
import { languageLabel } from "@/lib/languages";
import { requireSession } from "@/lib/session";

import { deleteScanAction } from "./actions";

type Params = { id: string };

export default async function ScanDetailPage({ params }: { params: Promise<Params> }) {
  const { id } = await params;
  const { token } = await requireSession();

  let scan;
  try {
    scan = await api.getScan(token, id);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) notFound();
    throw err;
  }

  const deleteAction = async () => {
    "use server";
    await deleteScanAction(id);
  };

  return (
    <div className="space-y-6">
      <header className="flex items-start justify-between gap-4">
        <div>
          <Link href="/app" className="text-sm text-ink-500 hover:underline">
            ← Back to scans
          </Link>
          <h1 className="mt-2 font-display text-3xl font-semibold">
            {scan.restaurant_name ?? "Menu"}
          </h1>
          <p className="mt-1 text-sm text-ink-500">
            Translated to {languageLabel(scan.target_language)} · {scan.dishes.length}{" "}
            {scan.dishes.length === 1 ? "dish" : "dishes"}
          </p>
        </div>

        <form action={deleteAction}>
          <button type="submit" className="btn-ghost text-sm">
            Delete scan
          </button>
        </form>
      </header>

      {scan.dishes.length === 0 ? (
        <div className="card p-8 text-center text-sm text-ink-500">
          We couldn&apos;t read any dishes from this photo. Try a clearer picture.
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {scan.dishes.map((dish) => (
            <DishCard key={dish.id} dish={dish} />
          ))}
        </div>
      )}
    </div>
  );
}
