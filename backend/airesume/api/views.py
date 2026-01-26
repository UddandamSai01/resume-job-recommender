import os,re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resume, Job
from .utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_skills,
    match_resume_to_job,
    normalize_text,
    SKILLS_DB,
)


@api_view(["POST"])
def upload_resume_file(request):
    if "resume_file" not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES["resume_file"]

    # Basic validation for file size
    if file.size > 2 * 1024 * 1024:
        return Response(
            {"error": "File too large. Max 2MB allowed"},
            status=400
        )

    resume = Resume.objects.create(resume_file=file)
    return Response({"message": "Uploaded successfully", "id": resume.id}, status=201)


@api_view(["GET"])
def analyze_resume(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return Response({"error": "Resume not found"}, status=404)

    if not resume.resume_file:
        return Response({"error": "Resume file missing"}, status=400)

    file_path = resume.resume_file.path

    if not os.path.exists(file_path):
        return Response({"error": "File not found on server"}, status=404)

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in [".doc", ".docx"]:
        text = extract_text_from_docx(file_path)
    else:
        return Response({"error": "Only PDF/DOCX supported"}, status=400)

    if not text.strip():
        return Response({"error": "Empty resume text"}, status=400)

    resume_skills = extract_skills(text)

    recommendations = []

    for job in Job.objects.all():
        
        raw = normalize_text(job.job_required_skills)

        job_skills = []

        for skill in SKILLS_DB:
            skill = skill.lower().strip()

            # Single-word skills (like c, sql, java)
            if " " not in skill and "." not in skill and "+" not in skill and "#" not in skill:
                pattern = rf"(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])"
                if re.search(pattern, raw):
                    job_skills.append(skill)

            # Multi-word / special skills
            else:
                if re.search(rf"(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])", raw):
                    job_skills.append(skill)


        score, matched = match_resume_to_job(resume_skills, job_skills)

        recommendations.append({
            "job_title": job.job_title,
            "company": job.company_name,
            "location": job.job_location,
            "salary": job.job_salary,
            "description": job.job_description,
            "apply_link": job.job_apply_link,
            "required_skills": sorted(job_skills),
            "match_score": score,
            "matched_skills": matched
        })

    return Response({
        "extracted_skills": resume_skills,
        "recommendations": sorted(
            recommendations,
            key=lambda x: x["match_score"],
            reverse=True
        )
    })
