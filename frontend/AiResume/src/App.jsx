import { BrowserRouter, Routes, Route } from "react-router-dom";
import ResumeUpload from "./ResumeUpload";
import Jobs from "./Jobs";
import AdminPanel from "./Adminpannel";
import AdminLogin from "./Adminlogin";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ResumeUpload />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/admin-panel" element={<AdminPanel />} />
        <Route path="/admin-login" element={<AdminLogin />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
