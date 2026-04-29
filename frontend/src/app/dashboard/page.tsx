import Sidebar from "@/components/Sidebar";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <main className="flex">
        <Sidebar />

        <section className="flex-1 p-8">
          <h1 className="text-3xl font-semibold mb-2">
            Dashboard
          </h1>

          <p className="text-gray-500 mb-8">
            Welcome to VisualAI
          </p>

          <div className="grid grid-cols-3 gap-5">
            <div className="card p-6">
              <p className="text-gray-500">Processed</p>
              <h2 className="text-3xl mt-2">124</h2>
            </div>

            <div className="card p-6">
              <p className="text-gray-500">Speed</p>
              <h2 className="text-3xl mt-2">0.4s</h2>
            </div>

            <div className="card p-6">
              <p className="text-gray-500">Accuracy</p>
              <h2 className="text-3xl mt-2">97%</h2>
            </div>
          </div>
        </section>
      </main>
    </ProtectedRoute>
  );
}
