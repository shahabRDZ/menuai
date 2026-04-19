import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "MenuAI — Translate any restaurant menu",
  description:
    "Point your camera at a menu and get every dish translated, described, and allergen-tagged.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
