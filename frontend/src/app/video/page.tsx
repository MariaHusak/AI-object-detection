"use client";

import { useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/axios";

export default function VideoPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [videoUrl, setVideoUrl] = useState<string>("");

  const uploadVideo = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await api.post("/video/process-async", formData);

      const id = res.data.task_id;
      setTaskId(id);
      setStatus("Processing...");

      pollStatus(id);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }

    setLoading(false);
  };

  const pollStatus = (id: string) => {
    const interval = setInterval(async () => {
      try {
        const res = await api.get(`/video/status/${id}`);
        const data = res.data;

        setStatus(data.status);

        if (data.status === "SUCCESS") {
          clearInterval(interval);
          const videoPath = data.result?.video;
          if (videoPath) {
            const normalizedPath = videoPath.replace(/\\/g, "/");
            setVideoUrl(`http://localhost:8000/${normalizedPath}`);
          }
        }

        if (data.status === "FAILURE") {
          clearInterval(interval);
          alert("Processing failed");
        }
      } catch (err) {
        console.error(err);
        clearInterval(interval);
      }
    }, 2000);
  };

  return (
    <ProtectedRoute>
      <main className="flex min-h-screen bg-black text-white">
        <Sidebar />

        <section className="flex-1 p-8">
          <div className="mb-6">
            <h1 className="text-2xl font-semibold">Video AI Processing</h1>
            <p className="text-sm text-gray-500">
              Async object detection & segmentation
            </p>
          </div>

          <div className="bg-[#111] border border-gray-800 p-6 rounded-xl mb-6">
            <input
              type="file"
              accept="video/*"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="mb-4"
            />

            <button
              onClick={uploadVideo}
              disabled={!file || loading}
              className="px-5 py-2 bg-white text-black rounded-md text-sm font-medium disabled:opacity-40"
            >
              {loading ? "Uploading..." : "Process Video"}
            </button>
          </div>

          {status && (
            <div className="bg-[#111] border border-gray-800 p-4 rounded-xl mb-6">
              <p className="text-gray-400 text-sm">Status: {status}</p>
            </div>
          )}

          {videoUrl && (
            <div className="bg-[#111] border border-gray-800 p-4 rounded-xl">
              <p className="text-sm text-gray-500 mb-2">Result Video</p>
              <video src={videoUrl} controls className="w-full rounded-lg" />
            </div>
          )}
        </section>
      </main>
    </ProtectedRoute>
  );
}