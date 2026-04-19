import clsx from "clsx";

import { FavoriteButton } from "@/components/favorite-button";
import type { Dish } from "@/lib/api";

type Props = {
  dish: Dish;
  showFavoriteButton?: boolean;
};

export function DishCard({ dish, showFavoriteButton = true }: Props) {
  return (
    <article className="card p-5">
      <header className="flex items-start justify-between gap-4">
        <div>
          {dish.name_translated && dish.name_translated !== dish.name_original ? (
            <>
              <p className="font-display text-lg font-semibold text-ink-900">
                {dish.name_translated}
              </p>
              <p className="text-sm text-ink-500">{dish.name_original}</p>
            </>
          ) : (
            <p className="font-display text-lg font-semibold text-ink-900">
              {dish.name_original}
            </p>
          )}
        </div>

        <div className="flex items-center gap-3">
          {formatPrice(dish)}
          {showFavoriteButton && (
            <FavoriteButton dishId={dish.id} isFavorite={dish.is_favorite} />
          )}
        </div>
      </header>

      {dish.description && (
        <p className="mt-3 text-sm leading-relaxed text-ink-700">{dish.description}</p>
      )}

      <div className="mt-4 flex flex-wrap gap-2 text-xs">
        {dish.category && <Pill>{dish.category}</Pill>}
        {dish.is_vegetarian && <Pill tone="green">Vegetarian</Pill>}
        {dish.is_vegan && <Pill tone="green">Vegan</Pill>}
        {typeof dish.spice_level === "number" && dish.spice_level > 0 && (
          <Pill tone="red">{"🌶️".repeat(Math.min(dish.spice_level, 3))}</Pill>
        )}
        {dish.allergens?.map((a) => (
          <Pill key={a} tone="amber">
            {a}
          </Pill>
        ))}
      </div>

      {dish.ingredients && dish.ingredients.length > 0 && (
        <p className="mt-3 text-xs text-ink-500">{dish.ingredients.join(" · ")}</p>
      )}
    </article>
  );
}

function formatPrice(dish: Dish): React.ReactNode {
  if (dish.price === null || dish.price === undefined) return null;
  const formatted = dish.currency
    ? new Intl.NumberFormat(undefined, { style: "currency", currency: dish.currency })
        .format(dish.price)
    : dish.price.toString();
  return <span className="text-sm font-medium text-ink-700">{formatted}</span>;
}

function Pill({
  children,
  tone = "neutral",
}: {
  children: React.ReactNode;
  tone?: "neutral" | "green" | "red" | "amber";
}) {
  return (
    <span
      className={clsx(
        "rounded-full px-2 py-0.5",
        tone === "neutral" && "bg-ink-100 text-ink-700",
        tone === "green" && "bg-emerald-100 text-emerald-800",
        tone === "red" && "bg-red-100 text-red-800",
        tone === "amber" && "bg-amber-100 text-amber-800",
      )}
    >
      {children}
    </span>
  );
}
