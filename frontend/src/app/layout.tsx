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
    <html lang="en">
      <body className="bg-[#0d0d0d] text-white antialiased">
        {children}
      </body>
    </html>
  );
}
