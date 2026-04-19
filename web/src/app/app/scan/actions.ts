"use server";

import { redirect } from "next/navigation";

import { api, ApiError } from "@/lib/api";
import { requireSession } from "@/lib/session";

export type ScanActionState = { error?: string } | null;

export async function scanMenuAction(
  _: ScanActionState,
  formData: FormData,
): Promise<ScanActionState> {
  const image = formData.get("image");
  if (!(image instanceof File) || image.size === 0) {
    return { error: "Please choose a menu photo to upload." };
  }

  const targetLanguage = formData.get("target_language")?.toString() || undefined;
  const restaurantName = formData.get("restaurant_name")?.toString().trim() || undefined;

  const { token } = await requireSession();

  let scanId: string;
  try {
    const scan = await api.scanMenu(token, {
      image,
      imageName: image.name,
      targetLanguage,
      restaurantName,
    });
    scanId = scan.id;
  } catch (err) {
    if (err instanceof ApiError) return { error: err.message };
    return { error: "Could not scan this image. Try a clearer photo." };
  }

  redirect(`/app/scans/${scanId}`);
}
