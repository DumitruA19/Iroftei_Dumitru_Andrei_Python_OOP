// src/components/Sidebar.jsx
import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();

  const linkClass = (path) =>
    `block px-4 py-2 rounded hover:bg-blue-500 hover:text-white ${
      location.pathname === path ? "bg-blue-600 text-white" : "text-gray-800"
    }`;

  return (
    <aside className="w-60 min-h-screen bg-blue-100 p-4 shadow-md fixed top-0 left-0">
      <h2 className="text-xl font-bold mb-6">🧠 Math App</h2>
      <nav className="space-y-2">
        <Link to="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>
        <Link to="/history" className={linkClass("/history")}>
          History
        </Link>
      </nav>
    </aside>
  );
}
