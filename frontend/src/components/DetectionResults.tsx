"use client";

type Item = {
  label?: string;
  conf?: number;
};

export default function DetectionResults({
  boxes,
}: {
  boxes: Item[];
}) {
  if (!boxes?.length) return null;

  const colors = [
    "#ffffff",
    "#999999",
    "#666666",
    "#444444",
    "#00ff99",
    "#00ccff",
  ];

  return (
    <div className="mt-6 bg-[#111] border border-gray-800 rounded-2xl p-6">
      {/* HEADER */}
      <div className="flex items-center justify-between mb-5">
        <span className="text-sm text-gray-400">
          Last detection
        </span>

        <div className="flex items-center gap-2 text-sm text-green-400">
          <span className="w-2 h-2 rounded-full bg-green-400"></span>
          Done
        </div>
      </div>

      {/* LIST */}
      <div className="space-y-3">
        {boxes.map((item, i) => {
          const percent = Math.round(
            (item.conf || 0) * 100
          );

          return (
            <div
              key={i}
              className="grid grid-cols-[16px_120px_1fr_50px] gap-3 items-center"
            >
              <div
                className="w-3 h-3 rounded-full"
                style={{
                  background:
                    colors[i % colors.length],
                }}
              />

              <div className="text-sm text-white truncate">
                {item.label}
              </div>

              <div className="h-2 bg-[#222] rounded-full overflow-hidden">
                <div
                  className="h-full bg-white rounded-full"
                  style={{
                    width: `${percent}%`,
                  }}
                />
              </div>

              <div className="text-sm text-gray-400 text-right">
                {percent}%
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
