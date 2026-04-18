import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import JobModal from "./JobModal";

export default function Jobs() {
  const location = useLocation();
  const navigate = useNavigate();

  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);

  // COLOR LOGIC
  const getScoreColor = (score) => {
    if (score >= 71) return "green";
    if (score >= 50) return "orange";
    if (score >= 0 && score < 50) return "red";
    return "gray";
  };

  // FILTER + SORT
  useEffect(() => {
    if (!location.state) {
      navigate("/");
    } else {
      const filteredJobs = location.state.recommendations
        .filter((job) => (job.match_score || 0) > 0) // ✅ only score > 0
        .sort((a, b) => (b.match_score || 0) - (a.match_score || 0)); // ✅ highest first

      setJobs(filteredJobs);
    }
  }, [location, navigate]);

  return (
    <>
      {/* 🔙 Back Button */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-4 right-4 mb-10 bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded-lg shadow"
      >
        ← Back
      </button>

      <div className="min-h-screen bg-gray-100 p-4 sm:p-6">
        <h2 className="text-2xl sm:text-3xl font-bold text-center mt-6 mb-8">
          Recommended Jobs
        </h2>

        {/*  Empty State */}
        {jobs.length === 0 && (
          <p className="text-center text-gray-500 text-lg">
            No matching jobs found 😔
          </p>
        )}

        {/* Job Cards */}
        <div className="grid gap-6 max-w-5xl mx-auto">
          {jobs.map((job, i) => (
            <div
              key={i}
              className="bg-white rounded-xl shadow-md p-5 sm:p-6 hover:shadow-lg transition"
            >
              <h3 className="text-lg sm:text-xl font-bold text-center mb-4">
                {job.company}
              </h3>

              <div className="flex justify-between text-sm sm:text-base mb-2">
                <span className="font-semibold">{job.job_title}</span>
                <span className="text-gray-500">{job.location}</span>
              </div>

              <div className="flex justify-between items-center mb-4 text-sm sm:text-base">
                <span>💰 {job.salary}</span>

                <span>
                  <b>Match Score:</b>{" "}
                  <span
                    style={{
                      color: getScoreColor(job.match_score || 0),
                      fontWeight: "bold",
                    }}
                  >
                    {job.match_score || 0}%
                  </span>
                </span>
              </div>

              <div className="flex justify-between gap-2">
                <button
                  onClick={() => setSelectedJob(job)}
                  className="flex-1 px-3 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 text-sm sm:text-base"
                >
                  View
                </button>

                <a
                  href={job.apply_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 text-center px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm sm:text-base"
                >
                  Apply
                </a>
              </div>
            </div>
          ))}
        </div>

        {/*  Modal */}
        {selectedJob && (
          <JobModal
            job={selectedJob}
            onClose={() => setSelectedJob(null)}
          />
        )}
      </div>
    </>
  );
}