import Link from "next/link";

import { AuthForm } from "@/components/auth-form";

import { loginAction } from "../actions";

export default function LoginPage() {
  return (
    <div className="card p-8">
      <h1 className="font-display text-2xl font-semibold">Welcome back</h1>
      <p className="mt-1 text-sm text-ink-500">Log in to pick up where you left off.</p>

      <div className="mt-6">
        <AuthForm mode="login" action={loginAction} />
      </div>

      <p className="mt-6 text-sm text-ink-500">
        No account yet?{" "}
        <Link href="/register" className="font-medium text-accent-600 hover:underline">
          Create one
        </Link>
      </p>
    </div>
  );
}
