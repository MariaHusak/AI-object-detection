"use client";

import { useState } from "react";
import api from "@/lib/axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import ThemeToggle from "@/components/ThemeToggle";

export default function LoginPage() {
  const router = useRouter();
  const setToken = useAuthStore((s) => s.setToken);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const res = await api.post("/auth/login", { username, password });
      setToken(res.data.access_token);
      router.push("/dashboard");
    } catch {
      alert("Login failed");
    }
  };

  return (
    <main
      style={{ background: "var(--background)", color: "var(--text)" }}
      className="min-h-screen flex items-center justify-center px-6 relative"
    >
      <div className="absolute top-4 right-4 w-36">
        <ThemeToggle />
      </div>

      <div
        style={{ background: "var(--surface)", border: "1px solid var(--border)" }}
        className="w-full max-w-md rounded-2xl p-8 shadow-xl"
      >
        <h1 className="text-3xl font-semibold mb-2">Welcome back</h1>
        <p style={{ color: "var(--muted)" }} className="mb-8">
          Sign in to VisualAI
        </p>

        <div className="space-y-4">
          <input
            placeholder="Username"
            style={{
              background: "var(--surface-2)",
              border: "1px solid var(--border)",
              color: "var(--text)",
            }}
            className="w-full rounded-lg px-4 py-3 outline-none transition"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="Password"
            type="password"
            style={{
              background: "var(--surface-2)",
              border: "1px solid var(--border)",
              color: "var(--text)",
            }}
            className="w-full rounded-lg px-4 py-3 outline-none transition"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            onClick={login}
            className="w-full bg-[#111] text-white rounded-lg py-3 font-medium hover:opacity-90 transition"
          >
            Sign In
          </button>
        </div>

        <div style={{ color: "var(--muted)" }} className="mt-6 text-center text-sm">
          Don't have an account?{" "}
          <Link href="/register" style={{ color: "var(--text)" }} className="hover:underline">
            Sign up
          </Link>
        </div>
      </div>
    </main>
  );
}