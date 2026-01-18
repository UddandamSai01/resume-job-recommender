import { BrowserRouter, Routes, Route } from "react-router-dom";
import ResumeUpload from "./ResumeUpload";
import Jobs from "./Jobs";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ResumeUpload />} />
        <Route path="/jobs" element={<Jobs />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
