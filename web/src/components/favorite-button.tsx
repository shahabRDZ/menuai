"use client";

import { useTransition } from "react";

import { toggleFavoriteAction } from "@/app/app/scans/[id]/actions";

type Props = {
  dishId: string;
  isFavorite: boolean;
};

export function FavoriteButton({ dishId, isFavorite }: Props) {
  const [pending, startTransition] = useTransition();

  return (
    <button
      type="button"
      onClick={() =>
        startTransition(async () => {
          await toggleFavoriteAction(dishId, isFavorite);
        })
      }
      disabled={pending}
      aria-pressed={isFavorite}
      aria-label={isFavorite ? "Remove from favorites" : "Save as favorite"}
      className="text-xl leading-none transition hover:scale-110 disabled:opacity-50"
    >
      {isFavorite ? "★" : "☆"}
    </button>
  );
}
