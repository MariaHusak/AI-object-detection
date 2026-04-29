"use client";

import { useEffect, useRef } from "react";

type Box = {
  x: number;
  y: number;
  w: number;
  h: number;
  label?: string;
  conf?: number;
};

export default function ImagePreview({
  imageUrl,
  boxes = [],
}: {
  imageUrl: string;
  boxes?: Box[];
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!imageUrl) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new Image();
    img.src = imageUrl;

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);

      (boxes || []).forEach((box) => {
        if (!box) return;

        ctx.strokeStyle = "#00ff99";
        ctx.lineWidth = 2;
        ctx.strokeRect(box.x, box.y, box.w, box.h);

        if (box.label) {
          ctx.fillStyle = "#00ff99";
          ctx.font = "14px Arial";
          ctx.fillText(
            `${box.label} ${
              box.conf
                ? (box.conf * 100).toFixed(0) + "%"
                : ""
            }`,
            box.x,
            box.y - 5
          );
        }
      });
    };
  }, [imageUrl, boxes]);

  return (
    <div className="bg-[#111] border border-gray-800 p-4 rounded-xl">
      <canvas
        ref={canvasRef}
        className="w-full rounded-lg"
      />
    </div>
  );
}
