import { useState } from "react";
import axios from "axios";
import Loader from "./Loader.jsx";
import { useNavigate } from "react-router-dom";


function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const API = "https://ai-resume-job-recommender-1.onrender.com";
  const navigate = useNavigate();


  const handleUpload = async () => {
    

    setResult(null);

    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("resume_file", file);

    try {
      setLoading(true);

      // 1️⃣ Upload resume
      const uploadRes = await axios.post(
        `${API}/api/upload-resume/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const resumeId = uploadRes.data.id;

      // 2️⃣ Analyze resume
      const analyzeRes = await axios.get(
        `${API}/api/analyze-resume/${resumeId}/`
      );

      setLoading(false);
      // small delay for loader effect
      setTimeout(() => {
        navigate("/jobs", { state: analyzeRes.data });
      }, 1500);
      setResult(analyzeRes.data);

    } catch (err) {
      console.error(err);
      alert("Error while processing resume");
      setLoading(false);
    }
  };

  return (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 px-4">
    <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-xl text-center">

      <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
        AI Resume Analyzer
      </h1>

      <p className="text-gray-500 mb-6">
        Upload your resume and get AI-powered job recommendations
      </p>

      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 mb-6">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-lg file:border-0
          file:text-sm file:font-semibold
          file:bg-blue-50 file:text-blue-700
          hover:file:bg-blue-100"
        />
      </div>

      <button
        onClick={handleUpload}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition"
      >
        Analyze Resume
      </button>

      {loading && <Loader />}
    </div>
  </div>
);

}

export default ResumeUpload;
