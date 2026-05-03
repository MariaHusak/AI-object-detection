"use client";
import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function DashboardPage() {
  const [stats, setStats] = useState({ processed: 0, avg_time: 0, avg_accuracy: 0 });

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    fetch("http://localhost:8000/stats", {
        headers: { Authorization: `Bearer ${token}` }
    })
        .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
        })
        .then(setStats)
        .catch(err => console.error("Stats fetch failed:", err));
  }, []);

  return (
    <ProtectedRoute>
      <main className="flex">
        <Sidebar />
        <section className="flex-1 p-8">
          <h1 className="text-3xl font-semibold mb-2">Dashboard</h1>
          <p className="text-gray-500 mb-8">Welcome to VisualAI</p>
          <div className="grid grid-cols-3 gap-5">
            <div className="card p-6">
              <p className="text-gray-500">Processed</p>
              <h2 className="text-3xl mt-2">{stats.processed}</h2>
            </div>
            <div className="card p-6">
              <p className="text-gray-500">Speed</p>
              <h2 className="text-3xl mt-2">{stats.avg_time.toFixed(3)}s</h2>
            </div>
            <div className="card p-6">
              <p className="text-gray-500">Accuracy</p>
              <h2 className="text-3xl mt-2">{Math.round(stats.avg_accuracy * 100)}%</h2>
            </div>
          </div>
        </section>
      </main>
    </ProtectedRoute>
  );
}