import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminPanel() {
  const navigate = useNavigate();

  useEffect(() => {
    const isAuth = localStorage.getItem("adminAuth");
    if (!isAuth) {
      navigate("/admin-login");
    }
  }, []);

  const [form, setForm] = useState({
    job_title: "",
    company_name: "",
    job_location: "",
    job_salary: "",
    job_description: "",
    job_required_skills: "",
    job_apply_link: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    for (let key in form) {
      if (!form[key]) {
        alert("Fill all fields ⚠️");
        return;
      }
    }

    setLoading(true);

    try {
      const res = await fetch(
        "https://ai-resume-job-recommender-nr9o.onrender.com/api/create-job/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert("Failed ❌");
      } else {
        alert("Job Added ✅");
        setForm({
          job_title: "",
          company_name: "",
          job_location: "",
          job_salary: "",
          job_description: "",
          job_required_skills: "",
          job_apply_link: "",
        });
      }
    } catch {
      alert("Server error ❌");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-6">

      {/* Top Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-3 mb-6">
        <h2 className="text-xl sm:text-2xl font-bold">Admin Panel</h2>

        <div className="flex gap-2">
          <button
            onClick={() => navigate("/")}
            className="bg-gray-700 text-white px-4 py-2 rounded-lg text-sm"
          >
            Home
          </button>

          <button
            onClick={() => {
              localStorage.removeItem("adminAuth");
              navigate("/admin-login");
            }}
            className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Form Card */}
      <div className="bg-white shadow-xl rounded-2xl p-4 sm:p-8 max-w-3xl mx-auto">

        <h3 className="text-lg sm:text-xl font-semibold mb-4 text-center">
          Add Job
        </h3>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input name="job_title" placeholder="Job Title" value={form.job_title} onChange={handleChange} className="w-full border p-3 rounded-lg text-sm sm:text-base" />

          <input name="company_name" placeholder="Company Name" value={form.company_name} onChange={handleChange} className="w-full border p-3 rounded-lg" />

          <input name="job_location" placeholder="Location" value={form.job_location} onChange={handleChange} className="w-full border p-3 rounded-lg" />

          <input name="job_salary" placeholder="Salary" value={form.job_salary} onChange={handleChange} className="w-full border p-3 rounded-lg" />

          <textarea name="job_description" placeholder="Job Description" value={form.job_description} onChange={handleChange} className="w-full border p-3 rounded-lg h-24" />

          <textarea name="job_required_skills" placeholder="Skills (comma separated)" value={form.job_required_skills} onChange={handleChange} className="w-full border p-3 rounded-lg h-20" />

          <input name="job_apply_link" placeholder="Apply Link" value={form.job_apply_link} onChange={handleChange} className="w-full border p-3 rounded-lg" />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold"
          >
            {loading ? "Adding..." : "Add Job"}
          </button>

        </form>
      </div>
    </div>
  );
}