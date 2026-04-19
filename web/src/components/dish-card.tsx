import clsx from "clsx";

import { FavoriteButton } from "@/components/favorite-button";
import type { Dish } from "@/lib/api";

type Props = {
  dish: Dish;
  showFavoriteButton?: boolean;
};

export function DishCard({ dish, showFavoriteButton = true }: Props) {
  const riskBorder =
    dish.allergen_risk === "high"
      ? "border-red-300"
      : dish.allergen_risk === "medium"
        ? "border-amber-300"
        : "border-ink-200";

  return (
    <article className={clsx("card p-5 border", riskBorder)}>
      <header className="flex items-start justify-between gap-4">
        <div className="min-w-0">
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

        <div className="flex shrink-0 items-center gap-2">
          {typeof dish.recommendation_score === "number" && (
            <ScoreBadge score={dish.recommendation_score} />
          )}
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
        {dish.is_halal_possible && <Pill tone="green">Halal-possible</Pill>}
        {typeof dish.spice_level === "number" && dish.spice_level > 0 && (
          <Pill tone="red">{"🌶️".repeat(Math.min(dish.spice_level, 3))}</Pill>
        )}
        {dish.allergen_risk && dish.allergen_risk !== "low" && (
          <Pill tone="red">{dish.allergen_risk} allergen risk</Pill>
        )}
        {dish.tourist_trap_risk === "high" && <Pill tone="amber">tourist trap risk</Pill>}
        {dish.local_popularity === "high" && <Pill tone="green">local favorite</Pill>}
        {dish.value_assessment === "expensive" && <Pill tone="amber">pricey</Pill>}
        {dish.value_assessment === "cheap" && <Pill tone="green">great value</Pill>}
        {dish.allergens?.map((a) => (
          <Pill key={a} tone="amber">
            {a}
          </Pill>
        ))}
      </div>

      {dish.hidden_risks && dish.hidden_risks.length > 0 && (
        <div className="mt-3 rounded-md border border-amber-200 bg-amber-50 p-2 text-xs text-amber-900">
          <p className="font-medium">Hidden risks</p>
          <ul className="mt-1 list-disc space-y-0.5 pl-4">
            {dish.hidden_risks.map((r) => (
              <li key={r}>{r}</li>
            ))}
          </ul>
        </div>
      )}

      {dish.cultural_context && (dish.cultural_context.origin || dish.cultural_context.tradition) && (
        <div className="mt-3 rounded-md bg-ink-100 p-2 text-xs text-ink-700">
          {dish.cultural_context.origin && (
            <p>
              <span className="font-medium">Origin:</span> {dish.cultural_context.origin}
            </p>
          )}
          {dish.cultural_context.tradition && (
            <p className="mt-1">{dish.cultural_context.tradition}</p>
          )}
        </div>
      )}

      {dish.ingredients && dish.ingredients.length > 0 && (
        <p className="mt-3 text-xs text-ink-500">{dish.ingredients.join(" · ")}</p>
      )}
    </article>
  );
}

function ScoreBadge({ score }: { score: number }) {
  const tone = score >= 85 ? "green" : score >= 70 ? "amber" : "red";
  return (
    <div
      className={clsx(
        "rounded-full px-2 py-0.5 text-xs font-semibold",
        tone === "green" && "bg-emerald-100 text-emerald-800",
        tone === "amber" && "bg-amber-100 text-amber-800",
        tone === "red" && "bg-red-100 text-red-800",
      )}
      title="MenuAI recommendation score"
    >
      {score}
    </div>
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
