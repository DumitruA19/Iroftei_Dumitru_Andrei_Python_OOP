// src/pages/Dashboard.jsx
import { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import {
  calculatePower,
  calculateFactorial,
  calculateFibonacci,
} from "../api/math";

export default function Dashboard() {
  const { token } = useAuth();
  const [x, setX] = useState("");
  const [y, setY] = useState("");
  const [result, setResult] = useState("");

  const handlePower = async () => {
    const res = await calculatePower({ x: Number(x), y: Number(y) }, token);
    setResult(res.result);
  };

  const handleFactorial = async () => {
    const res = await calculateFactorial({ x: Number(x) }, token);
    setResult(res.result);
  };

  const handleFibonacci = async () => {
    const res = await calculateFibonacci({ x: Number(x) }, token);
    setResult(res.result);
  };

  return (
    <div className="min-h-screen bg-gray-100 pl-60">
      <Navbar />
      <Sidebar />

      <main className="pt-20 px-6">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Power */}
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-lg font-semibold mb-4">Power</h2>
            <input
              type="number"
              placeholder="x"
              className="w-full border p-2 mb-2 rounded"
              value={x}
              onChange={(e) => setX(e.target.value)}
            />
            <input
              type="number"
              placeholder="y"
              className="w-full border p-2 mb-2 rounded"
              value={y}
              onChange={(e) => setY(e.target.value)}
            />
            <button
              onClick={handlePower}
              className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Calculate
            </button>
          </div>

          {/* Factorial */}
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-lg font-semibold mb-4">Factorial</h2>
            <input
              type="number"
              placeholder="x"
              className="w-full border p-2 mb-2 rounded"
              value={x}
              onChange={(e) => setX(e.target.value)}
            />
            <button
              onClick={handleFactorial}
              className="w-full bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              Calculate
            </button>
          </div>

          {/* Fibonacci */}
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-lg font-semibold mb-4">Fibonacci</h2>
            <input
              type="number"
              placeholder="x"
              className="w-full border p-2 mb-2 rounded"
              value={x}
              onChange={(e) => setX(e.target.value)}
            />
            <button
              onClick={handleFibonacci}
              className="w-full bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
            >
              Calculate
            </button>
          </div>
        </div>

        {result !== "" && (
          <div className="mt-8 bg-white p-4 rounded shadow text-center">
            <h4 className="text-lg font-semibold">Result:</h4>
            <p className="text-gray-700 mt-2">{result}</p>
          </div>
        )}
      </main>
    </div>
  );
}
