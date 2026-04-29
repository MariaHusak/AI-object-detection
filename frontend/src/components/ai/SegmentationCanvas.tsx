"use client";

import { useEffect, useRef, useState } from "react";

export default function SegmentationCanvas({ data }: any) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [selected, setSelected] = useState<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new Image();
    img.src = data.image_url;

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;

      ctx.drawImage(img, 0, 0);

      drawBoxes(ctx, data.detections);
    };
  }, [data]);

  const drawBoxes = (ctx: CanvasRenderingContext2D, detections: any[]) => {
    detections.forEach((det, index) => {
      const [x1, y1, x2, y2] = det.box;

      ctx.strokeStyle = selected === index ? "#00ff88" : "#888";
      ctx.lineWidth = selected === index ? 3 : 1;

      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

      ctx.fillStyle = "rgba(0,0,0,0.5)";
      ctx.fillText(det.label, x1, y1 - 5);
    });
  };

  const handleClick = (e: any) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const foundIndex = data.detections.findIndex((d: any) => {
      const [x1, y1, x2, y2] = d.box;
      return x >= x1 && x <= x2 && y >= y1 && y <= y2;
    });

    if (foundIndex !== -1) {
      setSelected(foundIndex);
    }
  };

  return (
    <div style={{ marginTop: 20 }}>
      <canvas
        ref={canvasRef}
        onClick={handleClick}
        style={{
          border: "1px solid #333",
          borderRadius: 12,
          maxWidth: "100%",
        }}
      />
    </div>
  );
}
