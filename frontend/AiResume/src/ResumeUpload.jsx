import { useState } from "react";
import axios from "axios";
import Loader from "./Loader.jsx";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const API = "https://ai-resume-job-recommender-1.onrender.com";


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
      setResult(analyzeRes.data);

    } catch (err) {
      console.error(err);
      alert("Error while processing resume");
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Analyze Resume</button>

      {loading && <Loader />}

      {result && (
        <div>
          <h3>Your Skills</h3>
          <ul>
            {result.extracted_skills.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <h3>Job Recommendations</h3>
          {result.recommendations.map((job, i) => (
            <div
              key={i}
              style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}
            >
              <p>
                <b>Company Name{job.job}</b> – {job.company}
              </p>

              <p>Match Score: {job.match_score}%</p>

              <p>
                Matched Skills:{" "}
                {Array.isArray(job.matched_skills)
                  ? job.matched_skills.join(", ")
                  : job.matched_skills}
              </p>

              <p>
                Required Skills:{" "}
                {Array.isArray(job.required_skills)
                  ? job.required_skills.join(", ")
                  : job.required_skills}
              </p>

              <p>
                <a
                  href={job.apply_link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Apply Here
                </a>
              </p>
              <p>Salary: {job.salary}</p>
              <p>Job Description: {job.description}</p>
              <p>Location: {job.location}</p>
            {console.log(job)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
