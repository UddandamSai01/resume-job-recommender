import "./JobModal.css";

function JobModal({ job, onClose }) {
  if (!job) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-container"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="modal-header">
          <h2>{job.company}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        {/* Scrollable Body */}
        <div className="modal-body">
          <p>{job.description}</p>

          <h4><strong>Matched Skills:</strong></h4>
          <p style={{ color: "green" }}>
            {job.matched_skills.join(", ") || "No Mateched Skills"}
          </p>

          <h4><strong>Required Skills:</strong></h4>
          <p style={{color: "yellow"}}>
            {job.required_skills.join(", ")}
          </p>
        </div>

        {/* Footer */}
        <div className="modal-footer">
          <a
            href={job.apply_link}
            target="_blank"
            rel="noopener noreferrer"
            className="apply-btn"
          >
            Apply Now
          </a>
        </div>
      </div>
    </div>
  );
}

export default JobModal;
