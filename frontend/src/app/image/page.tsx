"use client";

import { useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/axios";
import ImagePreview from "@/components/ImagePreview";
import DetectionResults from "@/components/DetectionResults";

type Tool = "detect" | "segment" | "cutout" | "replace-bg";

export default function ImagePage() {
  const [file, setFile] = useState<File | null>(null);
  const [tool, setTool] = useState<Tool>("detect");
  const [loading, setLoading] = useState(false);

  const [imageUrl, setImageUrl] = useState("");
  const [boxes, setBoxes] = useState<any[]>([]);
  const [cutoutUrls, setCutoutUrls] = useState<string[]>([]);

  const [bgFile, setBgFile] = useState<File | null>(null);
  const [bgResultUrl, setBgResultUrl] = useState("");

  const cutoutReady = cutoutUrls.length > 0;

  const normalizeUrls = (data: any): string[] => {
    if (!data) return [];
    if (Array.isArray(data)) return data;
    if (typeof data === "string") {
      return data.split(",").map((s) => s.trim());
    }
    return [];
  };

  const downloadImage = async (url: string) => {
    try {
      const res = await fetch(url);
      const blob = await res.blob();

      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "visualai-result.png";
      link.click();

      URL.revokeObjectURL(link.href);
    } catch (err) {
      console.error(err);
      alert("Download failed");
    }
  };

  const processImage = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const endpoint =
        tool === "detect"
          ? "/image/detect-preview"
          : tool === "segment"
          ? "/image/segment-preview"
          : "/image/cutout";

      const res = await api.post(endpoint, formData);
      const data = res.data;

      setImageUrl(data.image_url || data.result_image || "");
      setBoxes(data.boxes || data.detections || []);

      if (tool === "cutout") {
        const urls = normalizeUrls(data.cutouts || data.cutout);
        setCutoutUrls(urls);
      } else {
        setCutoutUrls([]);
      }

      setBgResultUrl("");
    } catch (err) {
      console.error(err);
      alert("Processing failed");
    }

    setLoading(false);
  };

  const replaceBackground = async () => {
    if (!bgFile || !cutoutReady) return;

    setLoading(true);
    setBgResultUrl("");

    try {
      const cutoutRes = await fetch(cutoutUrls[0]);
      const cutoutBlob = await cutoutRes.blob();

      const formData = new FormData();
      formData.append("cutout_file", cutoutBlob, "cutout.png");
      formData.append("bg_file", bgFile);

      const res = await api.post("/image/replace-background", formData);
      setBgResultUrl(res.data.result_image);
    } catch (err) {
      console.error(err);
      alert("Replace BG failed");
    }

    setLoading(false);
  };

  const TOOLS = [
    { id: "detect", label: "Detect" },
    { id: "segment", label: "Segment" },
    { id: "cutout", label: "Cutout" },
    { id: "replace-bg", label: "Replace BG", requiresCutout: true },
  ] as const;

  return (
    <ProtectedRoute>
      <main className="flex min-h-screen bg-black text-white">
        <Sidebar />

        <section className="flex-1 p-8">
          <div className="mb-6">
            <h1 className="text-2xl font-semibold">AI Vision Studio</h1>
            <p className="text-sm text-gray-500">
              Detect • Segment • Cutout • Replace BG
            </p>
          </div>

          <div className="flex gap-2 mb-6 flex-wrap">
            {TOOLS.map((t) => {
              const isLocked = t.id === "replace-bg" && !cutoutReady;
              const isActive = tool === t.id;

              return (
                <button
                  key={t.id}
                  onClick={() => !isLocked && setTool(t.id as Tool)}
                  disabled={isLocked}
                  className={`px-4 py-2 rounded-md text-sm border ${
                    isActive
                      ? "bg-white text-black border-white"
                      : isLocked
                      ? "border-gray-800 text-gray-700 cursor-not-allowed"
                      : "border-gray-700 text-gray-400 hover:border-gray-500 hover:text-white"
                  }`}
                >
                  {t.label}
                </button>
              );
            })}
          </div>

          {tool !== "replace-bg" && (
            <div className="bg-[#111] border border-gray-800 p-6 rounded-xl mb-6">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="mb-4"
              />

              <button
                onClick={processImage}
                disabled={!file || loading}
                className="px-5 py-2 bg-white text-black rounded-md text-sm"
              >
                {loading ? "Processing..." : "Run AI Model"}
              </button>
            </div>
          )}

          {tool === "replace-bg" && (
            <div className="bg-[#111] border border-gray-800 p-6 rounded-xl mb-6 space-y-4">
              <div className="bg-black border border-gray-700 rounded-lg p-2 w-fit">
                <img
                  src={cutoutUrls[0]}
                  className="h-32 object-contain rounded-md"
                />
              </div>

              <p className="text-sm text-gray-500">
                Upload background image
              </p>

              <input
                type="file"
                accept="image/*"
                onChange={(e) => setBgFile(e.target.files?.[0] || null)}
              />

              <button
                onClick={replaceBackground}
                disabled={!bgFile || loading}
                className="px-5 py-2 bg-white text-black rounded-md text-sm"
              >
                {loading ? "Processing..." : "Apply Background"}
              </button>
            </div>
          )}

          {loading && (
            <div className="bg-[#111] border border-gray-800 p-6 rounded-xl">
              AI is analyzing image...
            </div>
          )}

          {tool === "cutout" && imageUrl && (
            <div className="mt-6 grid grid-cols-2 gap-6">
              <div className="bg-[#111] border border-gray-800 p-4 rounded-xl">
                <p className="text-sm text-gray-500 mb-2">Original</p>
                <img src={imageUrl} className="rounded-lg w-full" />
              </div>

              <div className="bg-[#111] border border-gray-800 p-4 rounded-xl">
                <p className="text-sm text-gray-500 mb-2">Cutout</p>

                {cutoutUrls.map((url, i) => (
                  <div key={i} className="mb-4">
                    <img src={url} className="rounded-lg w-full mb-2" />

                    <button
                      onClick={() => downloadImage(url)}
                      className="px-4 py-2 bg-white text-black rounded-md text-sm"
                    >
                      Download
                    </button>
                  </div>
                ))}

                {cutoutReady && (
                  <button
                    onClick={() => setTool("replace-bg")}
                    className="mt-4 px-4 py-2 bg-white text-black rounded-md text-sm font-medium"
                  >
                    → Replace Background
                  </button>
                )}
              </div>
            </div>
          )}

          {tool === "replace-bg" && bgResultUrl && (
            <div className="mt-6 grid grid-cols-2 gap-6">
              <div className="bg-[#111] border border-gray-800 p-4 rounded-xl">
                <p className="text-sm text-gray-500 mb-2">Cutout</p>
                <img src={cutoutUrls[0]} className="rounded-lg w-full" />
              </div>

              <div className="bg-[#111] border border-gray-800 p-4 rounded-xl">
                <p className="text-sm text-gray-500 mb-2">
                  Background Replaced
                </p>

                <img src={bgResultUrl} className="rounded-lg w-full mb-3" />

                <button
                  onClick={() => downloadImage(bgResultUrl)}
                  className="px-4 py-2 bg-white text-black rounded-md text-sm"
                >
                  Download
                </button>
              </div>
            </div>
          )}

          {tool !== "cutout" && tool !== "replace-bg" && imageUrl && (
            <div className="mt-6 space-y-6">
              <ImagePreview imageUrl={imageUrl} boxes={boxes} />

              <button
                onClick={() => downloadImage(imageUrl)}
                className="px-5 py-3 bg-white text-black rounded-lg"
              >
                Download
              </button>

              {tool === "detect" && <DetectionResults boxes={boxes} />}
            </div>
          )}
        </section>
      </main>
    </ProtectedRoute>
  );
}