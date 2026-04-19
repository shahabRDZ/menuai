import Link from "next/link";

import { DishCard } from "@/components/dish-card";
import { api } from "@/lib/api";
import { requireSession } from "@/lib/session";

export default async function FavoritesPage() {
  const { token } = await requireSession();
  const dishes = await api.listFavorites(token);

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-3xl font-semibold">Favorites</h1>
        <p className="mt-1 text-sm text-ink-500">
          Dishes you saved across all your scans.
        </p>
      </header>

      {dishes.length === 0 ? (
        <div className="card flex flex-col items-center p-12 text-center">
          <p className="font-display text-lg font-semibold">No favorites yet</p>
          <p className="mt-2 max-w-sm text-sm text-ink-500">
            Tap the star next to a dish inside any scan to save it here.
          </p>
          <Link href="/app/scan" className="btn-primary mt-6">
            Scan a menu
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {dishes.map((dish) => (
            <DishCard key={dish.id} dish={dish} />
          ))}
        </div>
      )}
    </div>
  );
}
