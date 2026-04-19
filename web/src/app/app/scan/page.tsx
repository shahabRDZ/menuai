import { ScanForm } from "@/components/scan-form";
import { requireSession } from "@/lib/session";

import { scanMenuAction } from "./actions";

export default async function ScanPage() {
  const { user } = await requireSession();

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <header>
        <h1 className="font-display text-3xl font-semibold">Scan a menu</h1>
        <p className="mt-1 text-sm text-ink-500">
          Any language, any photo. We handle the rest.
        </p>
      </header>

      <div className="card p-6">
        <ScanForm
          defaultTargetLanguage={user.target_language}
          action={scanMenuAction}
        />
      </div>

      <p className="text-xs text-ink-500">
        Tip: good lighting and a flat page give the best results. A slight angle is fine.
      </p>
    </div>
  );
}
