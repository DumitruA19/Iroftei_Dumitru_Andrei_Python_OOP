// src/components/Navbar.jsx
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { logout, token } = useAuth();
  const navigate = useNavigate();

  let username = "Guest";
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      username = payload.sub || "Unknown";
    } catch {
      username = "Unknown";
    }
  }

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="bg-white border-b px-6 py-4 flex justify-end items-center shadow-sm fixed left-60 right-0 top-0 z-40">
      <div className="flex items-center gap-4">
        <span className="font-medium text-gray-700">{username}</span>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
        >
          Logout
        </button>
      </div>
    </header>
  );
}
