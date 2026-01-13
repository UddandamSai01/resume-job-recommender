import { useState } from "react";
import axios from "axios";
import Loader from './Loader.jsx'

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);


  const handleUpload = async () => {

    setResult(false);

    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("resume_file", file);

    try {
        
      setLoading(true);
     
      // 1️⃣ Upload resume
      const uploadRes = await axios.post(
        "https://ai-resume-job-recommender.onrender.com/api/upload-resume/",
        formData,
        { headers: {
            "Content-Type": "multipart/form-data",
          }
        }
      );

      const resumeId = uploadRes.data.id;
      console.log(uploadRes.data)

      // 2️⃣ Analyze resume
      const analyzeRes = await axios.post(
        `https://ai-resume-job-recommender.onrender.com/api/analyze-resume/${resumeId}/`
      );
 
      console.log(analyzeRes.data)
      setTimeout(()=>{
        setLoading(false);
        setResult(analyzeRes.data);
      },5000);
      

    } catch (err) {
      alert("Error while processing resume");
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Analyze Resume</button>

      {loading && <Loader/> }
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
            <div key={i} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
              <p><b>{job.job}</b> – {job.company}</p>
              {/* {console.log(job.matched_skills)} */}
              <p>Match Score: {job.match_score}%</p>
              <p>Matched Skills:{job.matched_skills.join(", ")}</p>
              <p>Required Skills: {job.required_skills.join(", ")}</p>
              <p>
                <a href={job.applyLink} target="_blank" rel="noopener noreferrer">Apply Here</a>
              </p>
              <p>{job.Description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
