"use client";

import Link from "next/link";
import ThemeToggle from "@/components/ThemeToggle";
import { useRouter } from "next/navigation";

export default function Sidebar() {
  const router = useRouter();

  const logout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <aside
      style={{
        background: "var(--surface)",
        borderRight: "1px solid var(--border)",
      }}
      className="sticky top-0 h-screen w-64 flex flex-col p-6"
    >
      {/* LOGO */}
      <div className="mb-10">
        <h1 className="text-2xl font-bold" style={{ color: "var(--text)" }}>
          VisualAI
        </h1>
      </div>

      {/* MENU */}
      <nav className="flex flex-col gap-2">
        <Link
          href="/dashboard"
          style={{ color: "var(--muted)" }}
          className="px-4 py-3 rounded-lg hover:opacity-100 transition sidebar-item"
        >
          Dashboard
        </Link>
        <Link
          href="/image"
          style={{ color: "var(--muted)" }}
          className="px-4 py-3 rounded-lg transition sidebar-item"
        >
          Image Tools
        </Link>
        <Link
          href="/video"
          style={{ color: "var(--muted)" }}
          className="px-4 py-3 rounded-lg transition sidebar-item"
        >
          Video Tools
        </Link>
      </nav>

      <div className="mt-auto flex flex-col gap-3">
        <ThemeToggle />

        <button
          onClick={logout}
          style={{ background: "var(--text)", color: "var(--background)" }}
          className="w-full px-4 py-3 rounded-lg font-medium hover:opacity-90 transition"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}