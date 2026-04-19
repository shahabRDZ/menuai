"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";

import { LANGUAGES } from "@/lib/languages";

type Props = {
  mode: "login" | "register";
  action: (state: { error?: string } | null, formData: FormData) => Promise<{ error?: string } | null>;
};

export function AuthForm({ mode, action }: Props) {
  const [state, formAction] = useActionState(action, null);

  return (
    <form action={formAction} className="space-y-4">
      {mode === "register" && (
        <Field label="Name (optional)">
          <input name="name" className="input" autoComplete="name" />
        </Field>
      )}

      <Field label="Email">
        <input
          name="email"
          type="email"
          required
          autoComplete="email"
          className="input"
          placeholder="you@example.com"
        />
      </Field>

      <Field label="Password">
        <input
          name="password"
          type="password"
          required
          minLength={mode === "register" ? 8 : undefined}
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          className="input"
        />
      </Field>

      {mode === "register" && (
        <Field label="Translate menus to">
          <select name="target_language" defaultValue="en" className="input">
            {LANGUAGES.map((l) => (
              <option key={l.code} value={l.code}>
                {l.label}
              </option>
            ))}
          </select>
        </Field>
      )}

      {state?.error && (
        <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {state.error}
        </p>
      )}

      <SubmitButton label={mode === "login" ? "Log in" : "Create account"} />
    </form>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="label mb-1">{label}</span>
      {children}
    </label>
  );
}

function SubmitButton({ label }: { label: string }) {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending} className="btn-primary w-full">
      {pending ? "Working…" : label}
    </button>
  );
}
