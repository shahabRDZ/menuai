"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { api } from "@/lib/api";
import { requireSession } from "@/lib/session";

export async function toggleFavoriteAction(dishId: string, currentlyFavorite: boolean) {
  const { token } = await requireSession();
  if (currentlyFavorite) {
    await api.removeFavorite(token, dishId);
  } else {
    await api.addFavorite(token, dishId);
  }
  revalidatePath("/app/scans/[id]", "page");
  revalidatePath("/app/favorites");
}

export async function deleteScanAction(scanId: string) {
  const { token } = await requireSession();
  await api.deleteScan(token, scanId);
  redirect("/app");
}
