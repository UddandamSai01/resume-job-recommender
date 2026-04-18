import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminPanel() {
  const navigate = useNavigate();

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

    // 🔥 Basic validation
    for (let key in form) {
      if (!form[key]) {
        alert("Please fill all fields ⚠️");
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
      console.log(data);

      if (!res.ok) {
        alert("Failed to add job ❌");
      } else {
        alert("Job Added Successfully ✅");

        // reset form
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
    } catch (error) {
      console.error(error);
      alert("Server error ❌");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      
      {/* Back Button */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-4 right-4 bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded-lg shadow"
      >
        ← Back
      </button>

      {/* Card */}
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-2xl">
        
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
          Add Job
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            name="job_title"
            placeholder="Job Title"
            value={form.job_title}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg focus:ring-2 focus:ring-blue-400"
          />

          <input
            name="company_name"
            placeholder="Company Name"
            value={form.company_name}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg"
          />

          <input
            name="job_location"
            placeholder="Location"
            value={form.job_location}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg"
          />

          <input
            name="job_salary"
            placeholder="Salary"
            value={form.job_salary}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg"
          />

          <textarea
            name="job_description"
            placeholder="Job Description"
            value={form.job_description}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg h-24"
          />

          <textarea
            name="job_required_skills"
            placeholder="Required Skills (comma separated)"
            value={form.job_required_skills}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg h-20"
          />

          <input
            name="job_apply_link"
            placeholder="Apply Link"
            value={form.job_apply_link}
            onChange={handleChange}
            className="w-full border p-3 rounded-lg"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition"
          >
            {loading ? "Adding..." : "Add Job"}
          </button>

        </form>
      </div>
    </div>
  );
}