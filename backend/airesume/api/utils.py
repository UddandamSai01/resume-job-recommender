import re
from PyPDF2 import PdfReader
from docx import Document

# ---------------- SKILLS DATABASE (WITH ALIASES) ---------------- #

SKILLS_DB = {

    # -------- Programming Languages --------
    "python": ["python"],
    "java": ["java"],
    "c": ["c"],
    "c++": ["c++"],
    "c#": ["c#", "c sharp"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],

    # -------- Web --------
    "html": ["html"],
    "css": ["css"],
    "bootstrap": ["bootstrap"],
    "tailwind css": ["tailwind", "tailwind css"],

    "react": ["react", "reactjs", "react.js"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs"],
    "next.js": ["next.js", "nextjs"],

    "node.js": ["node.js", "nodejs"],
    "express.js": ["express", "express.js"],

    "django": ["django"],
    "flask": ["flask"],
    "spring boot": ["spring", "spring boot"],

    "rest api": ["rest api", "restful api"],
    "graphql": ["graphql"],

    # -------- Databases --------
    "mysql": ["mysql"],
    "postgresql": ["postgres", "postgresql"],
    "mongodb": ["mongodb"],
    "sqlite": ["sqlite"],
    "oracle": ["oracle"],
    "sql server": ["sql server", "mssql"],
    "redis": ["redis"],
    "firebase": ["firebase"],

    # -------- Data Science & AI --------
    "data science": ["data science"],
    "data analysis": ["data analysis", "data analytics"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "nlp": ["nlp", "natural language processing"],

    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "keras": ["keras"],
    "pytorch": ["pytorch"],

    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel"],

    # -------- Cloud & DevOps --------
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "google cloud": ["gcp", "google cloud"],

    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "github actions": ["github actions"],

    "terraform": ["terraform"],
    "ansible": ["ansible"],

    "ci/cd": ["ci/cd", "ci cd"],
    "linux": ["linux"],
    "bash": ["bash"],
    "shell scripting": ["shell scripting", "shell"],

    "system design": ["system design"],

    # -------- Core CS --------
    "object oriented programming": [
        "oop", "oops", "object oriented programming", "object-oriented programming"
    ],
    "data structures and algorithms": [
        "dsa", "data structures", "data structures and algorithms", "algorithms"
    ],

    # -------- Cyber Security --------
    "cyber security": ["cyber security"],
    "network security": ["network security"],
    "ethical hacking": ["ethical hacking"],
    "penetration testing": ["penetration testing"],
    "cryptography": ["cryptography"],
    "malware analysis": ["malware analysis"],
    "firewall": ["firewall"],
    "siem": ["siem"],
    "ids": ["ids"],
    "ips": ["ips"],

    # -------- Networking --------
    "computer networks": ["computer networks"],
    "tcp/ip": ["tcp/ip"],
    "dns": ["dns"],
    "dhcp": ["dhcp"],
    "routing": ["routing"],
    "switching": ["switching"],
    "ccna": ["ccna"],
    "ccnp": ["ccnp"],

    # -------- Electronics (EEE) --------
    "embedded systems": ["embedded systems"],
    "iot": ["iot", "internet of things"],
    "microcontrollers": ["microcontrollers"],
    "arduino": ["arduino"],
    "raspberry pi": ["raspberry pi"],

    "vlsi": ["vlsi"],
    "verilog": ["verilog"],
    "system verilog": ["system verilog"],
    "fpga": ["fpga"],

    "matlab": ["matlab"],
    "simulink": ["simulink"],

    "power electronics": ["power electronics"],
    "control systems": ["control systems"],
    "signal processing": ["signal processing"],
    "power systems": ["power systems"],

    "digital electronics": ["digital electronics"],
    "analog electronics": ["analog electronics"],
    "pcb design": ["pcb design"],
    "electrical machines": ["electrical machines"],

    # -------- Soft Skills --------
    "communication": ["communication"],
    "teamwork": ["teamwork"],
    "problem solving": ["problem solving", "problem-solving"],
    "leadership": ["leadership"],
    "time management": ["time management"],
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
    text = re.sub(r"[^a-z0-9@.+#\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------- SKILL EXTRACTION ---------------- #

def extract_skills(text: str):
    text = normalize_text(text)
    found = set()

    for main_skill, variations in SKILLS_DB.items():
        for var in variations:
            pattern = rf"(?<![a-z0-9]){re.escape(var)}(?![a-z0-9])"
            if re.search(pattern, text):
                found.add(main_skill)
                break

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