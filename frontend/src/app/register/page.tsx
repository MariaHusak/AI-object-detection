"use client";

import { useState } from "react";
import api from "@/lib/axios";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const register = async () => {
    try {
      await api.post("/auth/register", {
        username,
        password,
      });

      router.push("/login");
    } catch {
      alert("Register failed");
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <div className="card w-full max-w-md p-8">
        <h1 className="text-3xl font-semibold mb-2">
          Create account
        </h1>

        <p className="text-gray-500 mb-8">
          Join VisualAI platform
        </p>

        <div className="space-y-4">
          <input
            className="input"
            placeholder="Username"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
          />

          <input
            className="input"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          <button
            onClick={register}
            className="btn btn-primary w-full"
          >
            Register
          </button>
        </div>
      </div>
    </main>
  );
}
