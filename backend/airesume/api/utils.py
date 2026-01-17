import re
from PyPDF2 import PdfReader
from docx import Document

SKILLS_DB = {
    # -------- Software Development --------
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "html", "css", "bootstrap", "tailwind css",
    "react", "angular", "vue", "next.js",
    "node.js", "express.js",
    "django", "flask", "spring boot",
    "rest api", "graphql",

    # -------- Databases --------
    "mysql", "postgresql", "mongodb", "sqlite",
    "oracle", "sql server", "redis", "firebase",

    # -------- Data Science & AI --------
    "data science", "data analysis", "data analytics",
    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "natural language processing",
    "pandas", "numpy", "matplotlib", "seaborn",
    "scikit-learn", "tensorflow", "keras", "pytorch",
    "power bi", "tableau", "excel",

    # -------- Cloud & DevOps --------
    "aws", "azure", "google cloud", "gcp",
    "docker", "kubernetes", "jenkins", "github actions",
    "terraform", "ansible",
    "ci/cd", "linux", "bash", "shell scripting",

    # -------- Cyber Security --------
    "cyber security", "network security", "ethical hacking",
    "penetration testing", "cryptography", "malware analysis",
    "firewall", "siem", "ids", "ips",

    # -------- Networking --------
    "computer networks", "tcp/ip", "dns", "dhcp",
    "routing", "switching", "ccna", "ccnp",

    # -------- Electronics / EEE --------
    "embedded systems", "iot", "internet of things",
    "microcontrollers", "arduino", "raspberry pi",
    "vlsi", "verilog", "system verilog", "fpga",
    "matlab", "simulink", "power electronics",
    "control systems", "signal processing",
    "digital electronics", "analog electronics", "pcb design",

    # -------- Mechanical --------
    "autocad", "solidworks", "catia", "ansys",
    "manufacturing", "production engineering",
    "thermodynamics", "fluid mechanics",
    "machine design", "industrial engineering",

    # -------- Civil --------
    "staad pro", "etabs", "autocad civil",
    "construction management", "surveying",
    "structural engineering", "geotechnical engineering",

    # -------- Business / Management --------
    "business analysis", "project management",
    "agile", "scrum", "jira",
    "digital marketing", "seo", "content marketing",
    "financial analysis", "accounting", "tally",
    "human resources", "operations management",

    # -------- General Tools --------
    "git", "github", "gitlab",
    "postman", "swagger",
    "confluence"
}


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return " ".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return " ".join(p.text for p in doc.paragraphs)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_skills(text: str):
    text = normalize_text(text)
    words = set(text.split())

    found = set()

    for skill in SKILLS_DB:
        if " " in skill:
            if re.search(rf"\b{re.escape(skill)}\b", text):
                found.add(skill)
        else:
            if skill in words:
                found.add(skill)

    return sorted(found)


def match_resume_to_job(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set & job_set

    if not job_set:
        return 0.0, 'No Sklls Found'
    
    if not matched:
        return 0.0, 'No Matched Skills Found'

    score = (len(matched) / len(job_set)) * 100
    return round(score, 2), sorted(matched)
