import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import JobModal from "./JobModal";

export default function Jobs() {
  const location = useLocation();
  const navigate = useNavigate();

  const getScoreColor = (score) => {
    if (score >= 71) return "green";
    if (score >= 50) return "orange";
    if (0 <= score < 50) return "red";
    return "gray";
  };


  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    // If user comes directly without data → redirect to home
    if (!location.state) {
      navigate("/");
    } else {
      setJobs(location.state.recommendations);
    }
  }, [location, navigate]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Back Button */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-4 right-4  bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded-lg shadow"
      >
        ← Back
      </button>

      <h2 className="text-3xl font-bold text-center mt-3 mb-8">
        Recommended Jobs
      </h2>

      <div className="grid gap-6 max-w-5xl mx-auto">
        {jobs.map((job, i) => (
          <div key={i} className="bg-white rounded-xl shadow-md p-6">

            <h3 className="text-xl font-bold text-center mb-4">
              {job.company}
            </h3>

            <div className="flex justify-between mb-2">
              <span className="font-semibold">{job.job_title}</span>
              <span className="text-gray-500">{job.location}</span>
            </div>

            <div className="flex justify-between mb-4">
              <span>💰 {job.salary}</span>
              <span>
                <b>Match Score:</b>{" "}
                <span style={{ color: getScoreColor(job.match_score || 0), fontWeight: "bold" }}>
                  {job.match_score || 0}%
                </span>
              </span>
            </div>

            <div className="flex justify-between">
              <button
                onClick={() => setSelectedJob(job)}
                className="px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50"
              >
                View
              </button>

              <a
                href={job.apply_link}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Apply
              </a>
            </div>
          </div>
        ))}
      </div>

      {selectedJob && (
        <JobModal job={selectedJob} onClose={() => setSelectedJob(null)} />
      )}
    </div>
  );
}
