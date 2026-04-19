"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";

import { LANGUAGES } from "@/lib/languages";

type Props = {
  defaultTargetLanguage: string;
  action: (
    state: { error?: string } | null,
    formData: FormData,
  ) => Promise<{ error?: string } | null>;
};

export function ImportForm({ defaultTargetLanguage, action }: Props) {
  const [state, formAction] = useActionState(action, null);

  return (
    <form action={formAction} className="space-y-5">
      <label className="block">
        <span className="label mb-1">Menu URL (from QR code)</span>
        <input
          name="url"
          type="url"
          required
          inputMode="url"
          autoComplete="url"
          placeholder="https://restaurant.com/menu"
          className="input"
        />
        <p className="mt-1 text-xs text-ink-500">
          Paste the link your restaurant&apos;s QR code opens to. Any page with menu text works.
        </p>
      </label>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="label mb-1">Translate to</span>
          <select
            name="target_language"
            defaultValue={defaultTargetLanguage}
            className="input"
          >
            {LANGUAGES.map((l) => (
              <option key={l.code} value={l.code}>
                {l.label}
              </option>
            ))}
          </select>
        </label>

        <label className="block">
          <span className="label mb-1">Restaurant (optional)</span>
          <input name="restaurant_name" className="input" placeholder="e.g. Çiya Sofrası" />
        </label>
      </div>

      {state?.error && (
        <p className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {state.error}
        </p>
      )}

      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending} className="btn-primary">
      {pending ? "Fetching menu…" : "Import this menu"}
    </button>
  );
}
