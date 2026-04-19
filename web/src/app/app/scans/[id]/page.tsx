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
            {scan.cuisine_type && <>{scan.cuisine_type} · </>}
            {scan.location && <>{scan.location} · </>}
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

      {(scan.ai_recommendations || scan.order_suggestions) && (
        <AiInsights
          recommendations={scan.ai_recommendations}
          orderSuggestions={scan.order_suggestions}
        />
      )}

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

function AiInsights({
  recommendations,
  orderSuggestions,
}: {
  recommendations: Awaited<ReturnType<typeof api.getScan>>["ai_recommendations"];
  orderSuggestions: Awaited<ReturnType<typeof api.getScan>>["order_suggestions"];
}) {
  return (
    <section className="grid gap-4 md:grid-cols-2">
      {recommendations && (
        <div className="card p-5">
          <h2 className="font-display text-lg font-semibold">MenuAI recommends</h2>
          {recommendations.best_for_user && recommendations.best_for_user.length > 0 && (
            <ul className="mt-3 space-y-2 text-sm">
              {recommendations.best_for_user.map((r, i) => (
                <li key={i}>
                  <p className="font-medium text-ink-900">{r.dish_name}</p>
                  <p className="text-ink-600">{r.reason}</p>
                </li>
              ))}
            </ul>
          )}
          {recommendations.avoid_if && recommendations.avoid_if.length > 0 && (
            <div className="mt-4 border-t border-ink-100 pt-3">
              <p className="text-sm font-medium text-ink-900">Avoid if</p>
              <ul className="mt-1 space-y-1 text-sm text-ink-600">
                {recommendations.avoid_if.map((a, i) => (
                  <li key={i}>
                    <span className="font-medium">{a.condition}</span> — {a.reason}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {orderSuggestions && (
        <div className="card p-5">
          <h2 className="font-display text-lg font-semibold">Ways to order</h2>
          <dl className="mt-3 space-y-2 text-sm">
            {orderSuggestions.light_option && (
              <Row label="Light">{orderSuggestions.light_option}</Row>
            )}
            {orderSuggestions.protein_rich_option && (
              <Row label="Protein-rich">{orderSuggestions.protein_rich_option}</Row>
            )}
            {orderSuggestions.budget_option && (
              <Row label="Budget">{orderSuggestions.budget_option}</Row>
            )}
            {orderSuggestions.local_experience_option && (
              <Row label="Local experience">{orderSuggestions.local_experience_option}</Row>
            )}
          </dl>
        </div>
      )}
    </section>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex gap-2">
      <dt className="w-28 shrink-0 text-ink-500">{label}</dt>
      <dd className="text-ink-900">{children}</dd>
    </div>
  );
}
