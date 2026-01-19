import "./Loader.css";

function Loader() {
  return (
    <div className="loader-overlay">
      <div className="loader-box">
        <div className="spinner"></div>
        <p>Analyzing your resume...</p>
      </div>
    </div>
  );
}

export default Loader;
