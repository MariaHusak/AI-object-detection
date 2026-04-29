"use client";

import { useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/axios";
import ImagePreview from "@/components/ImagePreview";
import DetectionResults from "@/components/DetectionResults";

type Tool = "detect" | "segment" | "cutout";

export default function ImagePage() {
  const [file, setFile] = useState<File | null>(null);
  const [tool, setTool] = useState<Tool>("detect");
  const [loading, setLoading] = useState(false);

  const [imageUrl, setImageUrl] = useState("");
  const [boxes, setBoxes] = useState<any[]>([]);
  const [cutoutUrls, setCutoutUrls] = useState<string[]>([]);

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
      const response = await fetch(url);
      const blob = await response.blob();

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
        const urls = normalizeUrls(
          data.cutouts || data.cutout
        );
        setCutoutUrls(urls);
      } else {
        setCutoutUrls([]);
      }
    } catch (err) {
      console.error(err);
      alert("Processing failed");
    }

    setLoading(false);
  };

  return (
    <ProtectedRoute>
      <main className="flex min-h-screen bg-black text-white">
        <Sidebar />

        <section className="flex-1 p-8">
          {/* HEADER */}
          <div className="mb-6">
            <h1 className="text-2xl font-semibold">
              AI Vision Studio
            </h1>

            <p className="text-sm text-gray-500">
              Detect • Segment • Cutout
            </p>
          </div>

          {/* TOOL SWITCH */}
          <div className="flex gap-2 mb-6">
            {[
              { id: "detect", label: "Detect" },
              { id: "segment", label: "Segment" },
              { id: "cutout", label: "Cutout" },
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setTool(t.id as Tool)}
                className={`px-4 py-2 rounded-md text-sm border transition ${
                  tool === t.id
                    ? "bg-white text-black border-white"
                    : "border-gray-700 text-gray-400 hover:border-gray-500 hover:text-white"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* UPLOAD */}
          <div className="bg-[#111] border border-gray-800 p-6 rounded-xl mb-6">
            <input
              type="file"
              accept="image/*"
              onChange={(e) =>
                setFile(e.target.files?.[0] || null)
              }
              className="mb-4"
            />

            <button
              onClick={processImage}
              disabled={!file || loading}
              className="px-5 py-2 bg-white text-black rounded-md text-sm font-medium disabled:opacity-40"
            >
              {loading
                ? "Processing AI..."
                : "Run AI Model"}
            </button>
          </div>

          {/* LOADING */}
          {loading && (
            <div className="bg-[#111] border border-gray-800 p-6 rounded-xl text-gray-400">
              AI is analyzing image...
            </div>
          )}

          {/* DETECT + SEGMENT */}
          {tool !== "cutout" && imageUrl && (
            <div className="mt-6 space-y-6">
              <ImagePreview
                imageUrl={imageUrl}
                boxes={boxes}
              />

              <button
                onClick={() =>
                  downloadImage(imageUrl)
                }
                className="px-5 py-3 bg-white text-black rounded-lg font-medium hover:opacity-90"
              >
                Download Result
              </button>

              {tool === "detect" && (
                <DetectionResults
                  boxes={boxes}
                />
              )}
            </div>
          )}

          {/* CUTOUT UI */}
          {tool === "cutout" && imageUrl && (
            <div className="mt-6 grid grid-cols-2 gap-6">
              {/* ORIGINAL */}
              <div className="bg-[#111] border border-gray-800 rounded-xl p-4">
                <p className="text-sm text-gray-500 mb-2">
                  Original
                </p>

                <img
                  src={imageUrl}
                  className="rounded-lg w-full"
                />
              </div>

              {/* CUTOUT RESULT */}
              <div className="bg-[#111] border border-gray-800 rounded-xl p-4">
                <p className="text-sm text-gray-500 mb-2">
                  AI Cutout Result
                </p>

                {cutoutUrls.length > 0 ? (
                  cutoutUrls.map((url, i) => (
                    <div
                      key={i}
                      className="mb-4"
                    >
                      <img
                        src={url}
                        className="rounded-lg w-full mb-2"
                      />

                      <button
                        onClick={() =>
                          downloadImage(url)
                        }
                        className="px-4 py-2 bg-white text-black rounded-md text-sm"
                      >
                        Download
                      </button>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-600 text-sm">
                    No cutout generated
                  </p>
                )}
              </div>
            </div>
          )}
        </section>
      </main>
    </ProtectedRoute>
  );
}
