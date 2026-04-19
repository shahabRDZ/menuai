import Link from "next/link";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-ink-50">
      <header className="border-b border-ink-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Link href="/" className="font-display text-xl font-semibold">
            MenuAI
          </Link>
        </div>
      </header>
      <main className="mx-auto flex max-w-md flex-col px-6 py-16">{children}</main>
    </div>
  );
}
