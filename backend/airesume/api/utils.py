import os,re
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


# ---------- TEXT EXTRACTION ----------

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_text(file_path):
    """
    Detect file type and extract text accordingly.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".doc", ".docx"]:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOC/DOCX.")


# ---------- SKILL EXTRACTION ----------

def extract_skills_from_resume(text):
    found_skills = set()

    # normalize text
    text_lower = text.lower()
    text_lower = text_lower.replace("\n", " ")
    text_lower = " ".join(text_lower.split())

    # normalize common variations
    text_lower = text_lower.replace("auto cad", "autocad")
    text_lower = text_lower.replace("ms office", "microsoft office")

    for category, skill_list in skills.items():
        for skill in skill_list:
            skill_lower = skill.lower()

            # 🚫 ignore single-letter skills like "c"
            # if len(skill_lower) == 1:
            #     continue

            # match only full words / phrases
            if f" {skill_lower} " in f" {text_lower} ":
                found_skills.add(skill)

    return list(found_skills)




# ---------- MATCHING LOGIC ----------

def match_resume_to_job(resume_skills, job_skills):
    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])

    if not job_set:
        return 0, "No matched skills"

    matched = resume_set.intersection(job_set)

    if not matched:
        return 0, "No matched skills"

    score = len(matched) / len(job_set) * 100
    return round(score, 2), list(matched)

