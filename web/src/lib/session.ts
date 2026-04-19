import { cookies } from "next/headers";

import { api, type User } from "@/lib/api";

const SESSION_COOKIE = "menuai_session";
const SESSION_MAX_AGE = 60 * 60 * 24 * 7;

export async function setSessionToken(token: string): Promise<void> {
  const store = await cookies();
  store.set(SESSION_COOKIE, token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: SESSION_MAX_AGE,
  });
}

export async function clearSession(): Promise<void> {
  const store = await cookies();
  store.delete(SESSION_COOKIE);
}

export async function getSessionToken(): Promise<string | null> {
  const store = await cookies();
  return store.get(SESSION_COOKIE)?.value ?? null;
}

export async function getCurrentUser(): Promise<User | null> {
  const token = await getSessionToken();
  if (!token) return null;
  try {
    return await api.me(token);
  } catch {
    return null;
  }
}

export async function requireSession(): Promise<{ token: string; user: User }> {
  const token = await getSessionToken();
  if (!token) {
    throw new UnauthenticatedError();
  }
  const user = await api.me(token);
  return { token, user };
}

export class UnauthenticatedError extends Error {
  constructor() {
    super("Unauthenticated");
    this.name = "UnauthenticatedError";
  }
}
