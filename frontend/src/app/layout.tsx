import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "VisualAI",
  description: "AI Object Detection Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        style={{ background: "var(--background)", color: "var(--text)" }}
        className="antialiased"
      >
        {children}
      </body>
    </html>
  );
}