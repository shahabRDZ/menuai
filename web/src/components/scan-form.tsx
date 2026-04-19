"use client";

import { useActionState, useState } from "react";
import { useFormStatus } from "react-dom";

import { LANGUAGES } from "@/lib/languages";

type Props = {
  defaultTargetLanguage: string;
  action: (
    state: { error?: string } | null,
    formData: FormData,
  ) => Promise<{ error?: string } | null>;
};

export function ScanForm({ defaultTargetLanguage, action }: Props) {
  const [state, formAction] = useActionState(action, null);
  const [preview, setPreview] = useState<string | null>(null);

  return (
    <form action={formAction} className="space-y-5">
      <div>
        <span className="label mb-2 block">Menu photo</span>
        <label
          htmlFor="image"
          className="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-md
                     border border-dashed border-ink-200 bg-white px-4 py-12 text-center
                     transition hover:border-accent-500"
        >
          {preview ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={preview} alt="Menu preview" className="max-h-72 rounded-md shadow" />
          ) : (
            <>
              <span className="text-4xl">📸</span>
              <span className="text-sm text-ink-700">Click to choose a photo</span>
              <span className="text-xs text-ink-500">or drag one in · JPG, PNG, WEBP, HEIC</span>
            </>
          )}
        </label>
        <input
          id="image"
          name="image"
          type="file"
          accept="image/*"
          capture="environment"
          required
          className="sr-only"
          onChange={(e) => {
            const file = e.target.files?.[0];
            setPreview(file ? URL.createObjectURL(file) : null);
          }}
        />
      </div>

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
      {pending ? "Reading the menu…" : "Scan this menu"}
    </button>
  );
}
