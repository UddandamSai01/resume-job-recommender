export default function JobModal({ job, close }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

      <div className="bg-white rounded-xl w-full max-w-2xl p-6 relative">

        <button
          onClick={close}
          className="absolute top-3 right-3 text-xl font-bold text-gray-500 hover:text-red-500"
        >
          ✕
        </button>

        <h2 className="text-2xl font-bold mb-4">{job.job}</h2>

        <p className="mb-4 text-gray-600">{job.description}</p>

        <h4 className="font-semibold">Matched Skills</h4>
        <p className="mb-3 text-green-600">
          {job.matched_skills.join(", ")}
        </p>

        <h4 className="font-semibold">Required Skills</h4>
        <p className="mb-6 text-gray-700">
          {job.required_skills.join(", ")}
        </p>

        <div className="text-right">
          <a
            href={job.apply_link}
            target="_blank"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Apply Now
          </a>
        </div>
      </div>
    </div>
  );
}
