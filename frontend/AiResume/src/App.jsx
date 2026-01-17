import React from 'react'
import ResumeUpload from './ResumeUpload.jsx'
import Loader from './Loader.jsx'

export default function App() {
  return (
    <div style={{padding:"30px"}}>
      <h1>AI Resume Analyzer</h1>
      <ResumeUpload />
      {/* <Loader/> */}
    </div>
    
  )
}
