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
    "rest api", "graphql","reactjs", "angularjs", "vuejs",

    # -------- Databases --------
    "mysql", "postgresql", "mongodb", "sqlite",
    "oracle", "sql server", "redis", "firebase",

    # -------- Data Science & AI --------
    "data science", "data analysis", "data analytics",
    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "natural language processing",
    "pandas", "numpy", "matplotlib", "seaborn",
    "scikit-learn", "tensorflow", "keras", "pytorch",
    "power bi", "tableau", "excel", "sklearn", "ml",

    # -------- Cloud & DevOps --------
    "aws", "azure", "google cloud", "gcp",
    "docker", "kubernetes", "jenkins", "github actions",
    "terraform", "ansible",
    "ci/cd", "linux", "bash", "shell scripting", "algorithms", "system design",

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
    "control systems", "signal processing", "power systems",
    "digital electronics", "analog electronics", "pcb design",
    "electrical machines",

    # -------- Mechanical --------
    "autocad", "solidworks", "catia", "ansys",
    "manufacturing", "production", "quality",
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
    "confluence",

    # --------- common skills ---------
    "communication", "teamwork", "problem-solving",
    "site management", "engineering", "leadership", "time management",
}



# ---------------- TEXT EXTRACTION ---------------- #

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return " ".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return " ".join(p.text for p in doc.paragraphs)


# ---------------- NORMALIZATION ---------------- #

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\n\r\t]", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------- SKILL EXTRACTION (FIXED) ---------------- #

def extract_skills(text: str):
    text = normalize_text(text)

    # Tokenize resume into TRUE words
    tokens = set(text.split())

    found = set()

    for skill in SKILLS_DB:
        skill = skill.lower().strip()

        # 1-word skills → exact token match only
        if " " not in skill and "." not in skill and "+" not in skill and "#" not in skill:
            if skill in tokens:
                found.add(skill)

        # multi-word / special skills → strict regex
        else:
            escaped = re.escape(skill)
            pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
            if re.search(pattern, text):
                found.add(skill)

    return sorted(found)


# ---------------- MATCHING ---------------- #

def match_resume_to_job(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set & job_set

    if not job_set:
        return 0.0, []

    score = (len(matched) / len(job_set)) * 100
    return round(score, 2), sorted(matched)
