import { useLocation } from "react-router-dom";
import { useState } from "react";
import JobModal from "./JobModal";

export default function Jobs() {
  const { state } = useLocation();
  const [selectedJob, setSelectedJob] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-8">
        Recommended Jobs
      </h2>

      <div className="grid gap-6 max-w-5xl mx-auto">
        {state.recommendations.map((job, i) => (
          <div key={i} className="bg-white rounded-xl shadow-md p-6">

            <h3 className="text-xl font-bold text-center mb-4">
              {job.company}
            </h3>

            <div className="flex justify-between mb-2">
              <span className="font-semibold">{job.job}</span>
              <span className="text-gray-500">{job.location}</span>
            </div>

            <div className="flex justify-between mb-4">
              <span>💰 {job.salary}</span>
              <span className="text-green-600 font-bold">
                {job.match_score}% Match
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
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Apply
              </a>
            </div>
          </div>
        ))}
      </div>

      {selectedJob && (
        <JobModal job={selectedJob} close={() => setSelectedJob(null)} />
      )}
    </div>
  );
}
