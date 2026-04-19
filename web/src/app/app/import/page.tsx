import { ImportForm } from "@/components/import-form";
import { requireSession } from "@/lib/session";

import { importMenuAction } from "./actions";

export default async function ImportPage() {
  const { user } = await requireSession();

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <header>
        <h1 className="font-display text-3xl font-semibold">Import a QR-code menu</h1>
        <p className="mt-1 text-sm text-ink-500">
          Paste the URL your restaurant&apos;s QR code opens to. We&apos;ll fetch, translate,
          and tag every dish.
        </p>
      </header>

      <div className="card p-6">
        <ImportForm defaultTargetLanguage={user.target_language} action={importMenuAction} />
      </div>

      <div className="rounded-md border border-ink-200 bg-white p-4 text-sm text-ink-700">
        <p className="font-medium text-ink-900">Works with</p>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-ink-600">
          <li>Public HTML menu pages (most QR-code setups)</li>
          <li>JSON endpoints that expose the menu</li>
          <li>Plain-text menus</li>
        </ul>
        <p className="mt-3 text-xs text-ink-500">
          PDF and image-only menus? Use the photo scan flow instead.
        </p>
      </div>
    </div>
  );
}
