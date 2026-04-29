"use client";

import { useState } from "react";
import api from "@/lib/axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";

export default function LoginPage() {
  const router = useRouter();
  const setToken = useAuthStore((s) => s.setToken);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const res = await api.post("/auth/login", {
        username,
        password,
      });

      setToken(res.data.access_token);
      router.push("/dashboard");
    } catch {
      alert("Login failed");
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center px-6">
      <div className="w-full max-w-md bg-[#111] border border-gray-800 rounded-2xl p-8 shadow-xl">
        {/* HEADER */}
        <h1 className="text-3xl font-semibold mb-2">
          Welcome back
        </h1>

        <p className="text-gray-500 mb-8">
          Sign in to VisualAI
        </p>

        {/* FORM */}
        <div className="space-y-4">
          <input
            placeholder="Username"
            className="w-full bg-black border border-gray-800 rounded-lg px-4 py-3 outline-none focus:border-white transition"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
          />

          <input
            placeholder="Password"
            type="password"
            className="w-full bg-black border border-gray-800 rounded-lg px-4 py-3 outline-none focus:border-white transition"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          <button
            onClick={login}
            className="w-full bg-white text-black rounded-lg py-3 font-medium hover:opacity-90 transition"
          >
            Sign In
          </button>
        </div>

        {/* REGISTER LINK */}
        <div className="mt-6 text-center text-sm text-gray-500">
          Don’t have an account?{" "}
          <Link
            href="/register"
            className="text-white hover:underline"
          >
            Sign up
          </Link>
        </div>
      </div>
    </main>
  );
}
