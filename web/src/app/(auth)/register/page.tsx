import Link from "next/link";

import { AuthForm } from "@/components/auth-form";

import { registerAction } from "../actions";

export default function RegisterPage() {
  return (
    <div className="card p-8">
      <h1 className="font-display text-2xl font-semibold">Create your account</h1>
      <p className="mt-1 text-sm text-ink-500">Start translating menus in under a minute.</p>

      <div className="mt-6">
        <AuthForm mode="register" action={registerAction} />
      </div>

      <p className="mt-6 text-sm text-ink-500">
        Already have an account?{" "}
        <Link href="/login" className="font-medium text-accent-600 hover:underline">
          Log in
        </Link>
      </p>
    </div>
  );
}
