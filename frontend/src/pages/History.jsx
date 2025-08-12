// src/pages/History.jsx
import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import axios from "../api/axios";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function History() {
  const { token } = useAuth();
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await axios.get("/history", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history", err);
    }
  };

  const deleteEntry = async (id) => {
    try {
      await axios.delete(`/history/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error("Failed to delete entry", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const grouped = history.reduce((acc, item) => {
    const op = item.operation;
    if (!acc[op]) acc[op] = [];
    acc[op].push(item);
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-gray-100 pl-60">
      <Navbar />
      <Sidebar />

      <main className="pt-20 px-6">
        <h1 className="text-2xl font-bold mb-6">History</h1>

        {Object.entries(grouped).map(([operation, entries]) => (
          <div key={operation} className="mb-8">
            <h2 className="text-xl font-semibold mb-2 capitalize">{operation}</h2>
            <div className="bg-white shadow rounded p-4">
              {entries.map((entry) => (
                <div
                  key={entry.id}
                  className="flex justify-between items-center border-b py-2"
                >
                  <div>
                    <p className="text-sm text-gray-600">Input: {entry.input_data}</p>
                    <p className="text-sm text-gray-800">Result: {entry.result}</p>
                    <p className="text-xs text-gray-400">
                      Time: {new Date(entry.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <button
                    onClick={() => deleteEntry(entry.id)}
                    className="text-red-500 hover:text-red-700 font-semibold"
                  >
                    Delete
                  </button>
                </div>
              ))}
              {entries.length === 0 && <p>No entries yet.</p>}
            </div>
          </div>
        ))}
      </main>
    </div>
  );
}
