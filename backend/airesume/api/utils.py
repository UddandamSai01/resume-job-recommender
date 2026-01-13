from PyPDF2 import PdfReader
from docx import Document

skills = {
  "programming": [
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "Go", "Rust"
  ],

  "web_development": [
    "HTML", "CSS", "React", "Angular", "Vue.js",
    "Node.js", "Express.js", "Next.js",
    "REST API", "GraphQL"
  ],

  "database": [
    "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "Oracle", "SQLite", "Firebase"
  ],

  "data_ai": [
    "Data Analysis", "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "NLP", "Computer Vision",
    "Pandas", "NumPy", "Scikit-learn",
    "TensorFlow", "PyTorch",
    "Power BI", "Tableau", "Excel"
  ],

  "cloud_devops": [
    "AWS", "Azure", "Google Cloud",
    "Docker", "Kubernetes",
    "CI/CD", "Jenkins", "GitHub Actions",
    "Linux", "Shell Scripting"
  ],

  "software_testing": [
    "Manual Testing", "Automation Testing",
    "Selenium", "Cypress",
    "API Testing", "Postman",
    "Unit Testing", "Jest"
  ],

  "cyber_security": [
    "Network Security", "Ethical Hacking",
    "Penetration Testing", "Vulnerability Assessment",
    "SIEM", "Firewalls"
  ],

  "eee": [
    "Electrical Machines", "Power Systems",
    "Power Electronics", "Control Systems",
    "PLC", "SCADA",
    "MATLAB", "Simulink",
    "Embedded Systems", "PCB Design",
    "VLSI", "Renewable Energy"
  ],

  "mechanical": [
    "AutoCAD", "SolidWorks", "CATIA",
    "ANSYS", "Thermodynamics",
    "Fluid Mechanics", "Heat Transfer",
    "CNC Programming", "Quality Control",
    "Production Planning"
  ],

  "civil": [
    "AutoCAD", "STAAD Pro", "ETABS",
    "Surveying", "Structural Analysis",
    "Construction Management",
    "Estimation & Costing",
    "Site Supervision",
    "Safety Management"
  ],

  "electronics": [
    "Digital Electronics", "Analog Circuits",
    "Microcontrollers", "Arduino", "Raspberry Pi",
    "Embedded C", "IoT",
    "Verilog", "VHDL",
    "Signal Processing"
  ],

  "business_management": [
    "Project Management", "Business Analysis",
    "Operations Management",
    "Supply Chain Management",
    "Digital Marketing",
    "Financial Analysis",
    "HR Management"
  ],

  "soft_skills": [
    "Communication Skills", "Teamwork",
    "Leadership", "Problem Solving",
    "Critical Thinking", "Time Management",
    "Adaptability", "Decision Making"
  ]
}


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_skills(text):
    found_skills = []
    text = text.lower()
    for category in skills:
        for skill in skills[category]:
            if skill.lower() in text:
                found_skills.append(skill)
    return list(set(found_skills))

def match_resume_to_job(resume_skills, job_skills):
    # normalize both lists to lowercase
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    matched = resume_set.intersection(job_set)

    if not job_set:
        return 0, []

    score = len(matched) / len(job_set) * 100
    return round(score, 2), list(matched)
