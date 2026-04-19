"use server";

import { redirect } from "next/navigation";

import { api, ApiError } from "@/lib/api";
import { clearSession, setSessionToken } from "@/lib/session";

export type AuthActionState = { error?: string } | null;

export async function loginAction(_: AuthActionState, formData: FormData): Promise<AuthActionState> {
  const email = formData.get("email")?.toString().trim();
  const password = formData.get("password")?.toString();

  if (!email || !password) {
    return { error: "Email and password are required" };
  }

  try {
    const { access_token } = await api.login(email, password);
    await setSessionToken(access_token);
  } catch (err) {
    if (err instanceof ApiError) return { error: err.message };
    return { error: "Something went wrong. Try again." };
  }
  redirect("/app");
}

export async function registerAction(
  _: AuthActionState,
  formData: FormData,
): Promise<AuthActionState> {
  const email = formData.get("email")?.toString().trim();
  const password = formData.get("password")?.toString();
  const name = formData.get("name")?.toString().trim() || undefined;
  const target_language = formData.get("target_language")?.toString() || "en";

  if (!email || !password) {
    return { error: "Email and password are required" };
  }
  if (password.length < 8) {
    return { error: "Password must be at least 8 characters" };
  }

  try {
    const { access_token } = await api.register({
      email,
      password,
      name,
      target_language,
      native_language: target_language,
    });
    await setSessionToken(access_token);
  } catch (err) {
    if (err instanceof ApiError) return { error: err.message };
    return { error: "Something went wrong. Try again." };
  }
  redirect("/app");
}

export async function logoutAction(): Promise<void> {
  await clearSession();
  redirect("/");
}
