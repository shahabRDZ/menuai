"use server";

import { redirect } from "next/navigation";

import { api, ApiError } from "@/lib/api";
import { getSessionToken } from "@/lib/session";

export type ImportActionState = { error?: string } | null;

export async function importMenuAction(
  _: ImportActionState,
  formData: FormData,
): Promise<ImportActionState> {
  const url = formData.get("url")?.toString().trim();
  if (!url) return { error: "Paste a menu URL — the one your QR code leads to." };
  if (!/^https?:\/\//i.test(url)) {
    return { error: "URL must start with http:// or https://" };
  }

  const token = await getSessionToken();
  if (!token) return { error: "Session expired. Please log in again." };

  const targetLanguage = formData.get("target_language")?.toString() || undefined;
  const restaurantName = formData.get("restaurant_name")?.toString().trim() || undefined;

  let scanId: string | undefined;
  try {
    const scan = await api.importMenu(token, {
      url,
      targetLanguage,
      restaurantName,
    });
    scanId = scan?.id;
  } catch (err) {
    if (err instanceof ApiError) return { error: err.message };
    return { error: "Could not import that URL. Is the page reachable?" };
  }

  if (!scanId) return { error: "Import succeeded but returned no ID." };
  redirect(`/app/scans/${scanId}`);
}
