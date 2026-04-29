"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Sidebar() {
  const router = useRouter();

  const logout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <aside
      className="
        sticky top-0
        h-screen
        w-64
        bg-[#0f0f0f]
        border-r border-gray-800
        flex flex-col
        p-6
      "
    >
      {/* LOGO */}
      <div className="mb-10">
        <h1 className="text-2xl font-bold text-white">
          VisualAI
        </h1>
      </div>

      {/* MENU */}
      <nav className="flex flex-col gap-2">
        <Link
          href="/dashboard"
          className="px-4 py-3 rounded-lg text-gray-300 hover:bg-[#1a1a1a] hover:text-white transition"
        >
          Dashboard
        </Link>

        <Link
          href="/image"
          className="px-4 py-3 rounded-lg text-gray-300 hover:bg-[#1a1a1a] hover:text-white transition"
        >
          Image Tools
        </Link>

        <Link
          href="/video"
          className="px-4 py-3 rounded-lg text-gray-300 hover:bg-[#1a1a1a] hover:text-white transition"
        >
          Video Tools
        </Link>
      </nav>

      {/* PUSH DOWN */}
      <div className="mt-auto pt-6">
        <button
          onClick={logout}
          className="
            w-full
            px-4 py-3
            rounded-lg
            bg-white
            text-black
            font-medium
            hover:opacity-90
            transition
          "
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
