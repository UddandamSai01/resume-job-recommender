import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";

export default function AdminPanel() {
  const [form, setForm] = useState({
    job_title: "",
    company_name: "",
    job_location: "",
    job_salary: "",
    job_description: "",
    job_required_skills: "",
    job_apply_link: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const res = await fetch("https://ai-resume-job-recommender-nr9o.onrender.com/api/jobs/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    console.log(data);
    alert("Job Added Successfully ✅");
  };

  return (
    <div>
        <div className="absolute top-4 right-4">
          <button onClick={() => navigate("/")} className="bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg">
            <ArrowLeftIcon className="w-5 h-5" />
          </button>
        </div>

      <h2>Add Job</h2>

      <input name="job_title" placeholder="Job Title" onChange={handleChange} />
      <input name="company_name" placeholder="Company" onChange={handleChange} />
      <input name="job_location" placeholder="Location" onChange={handleChange} />
      <input name="job_salary" placeholder="Salary" onChange={handleChange} />

      <textarea name="job_description" placeholder="Description" onChange={handleChange}></textarea>
      <textarea name="job_required_skills" placeholder="Skills" onChange={handleChange}></textarea>

      <input name="job_apply_link" placeholder="Apply Link" onChange={handleChange} />

      <button onClick={handleSubmit}>Add Job</button>
    </div>
  );
}