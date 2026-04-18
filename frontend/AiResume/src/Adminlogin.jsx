import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminLogin() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = (e) => {
    e.preventDefault();

    if (form.username === "airesumeproject" && form.password === "airesume@2026") {
      localStorage.setItem("adminAuth", "true");
      navigate("/admin-panel");
    } else {
      setError("Invalid credentials ❌");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-indigo-600 px-4">
      
      <div className="bg-white w-full max-w-md rounded-2xl shadow-xl p-6 sm:p-8">

        <h2 className="text-xl sm:text-2xl font-bold text-center mb-6">
          Admin Login
        </h2>

        <form onSubmit={handleLogin} className="space-y-4">

          <div>
            <label className="text-sm text-gray-600">Username</label>
            <input
              type="text"
              name="username"
              placeholder="Enter username"
              value={form.username}
              onChange={handleChange}
              className="w-full mt-1 border p-3 rounded-lg focus:ring-2 focus:ring-blue-400 text-sm sm:text-base"
            />
          </div>

          <div>
            <label className="text-sm text-gray-600">Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter password"
              value={form.password}
              onChange={handleChange}
              className="w-full mt-1 border p-3 rounded-lg focus:ring-2 focus:ring-blue-400 text-sm sm:text-base"
            />
          </div>

          {error && (
            <p className="text-red-500 text-sm text-center">{error}</p>
          )}

          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold">
            Login
          </button>

        </form>
      </div>
    </div>
  );
}