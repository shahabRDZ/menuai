"use server";

import { redirect } from "next/navigation";

import { api, ApiError } from "@/lib/api";
import { getSessionToken } from "@/lib/session";

export type ScanActionState = { error?: string } | null;

export async function scanMenuAction(
  _: ScanActionState,
  formData: FormData,
): Promise<ScanActionState> {
  const image = formData.get("image");
  if (!(image instanceof File) || image.size === 0) {
    return { error: "Please choose a menu photo to upload." };
  }

  const token = await getSessionToken();
  if (!token) {
    return { error: "Session expired. Please log in again." };
  }

  const targetLanguage = formData.get("target_language")?.toString() || undefined;
  const restaurantName = formData.get("restaurant_name")?.toString().trim() || undefined;

  let scanId: string | undefined;
  try {
    const scan = await api.scanMenu(token, {
      image,
      imageName: image.name,
      targetLanguage,
      restaurantName,
    });
    scanId = scan?.id;
  } catch (err) {
    if (err instanceof ApiError) return { error: err.message };
    return { error: "Could not scan this image. Try a clearer photo." };
  }

  if (!scanId) {
    return { error: "Scan succeeded but returned no ID." };
  }

  redirect(`/app/scans/${scanId}`);
}
