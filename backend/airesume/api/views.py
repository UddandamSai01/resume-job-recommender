import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Resume, Job
from .utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_skills,
    match_resume_to_job,
)


# ---------------- UPLOAD RESUME ---------------- #

@api_view(["POST"])
def upload_resume_file(request):
    if "resume_file" not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES["resume_file"]

    # File size validation (2MB)
    if file.size > 2 * 1024 * 1024:
        return Response(
            {"error": "File too large. Max 2MB allowed"},
            status=400
        )

    # File type validation
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in [".pdf", ".doc", ".docx"]:
        return Response(
            {"error": "Only PDF/DOC/DOCX files are allowed"},
            status=400
        )

    resume = Resume.objects.create(resume_file=file)

    return Response({
        "message": "Uploaded successfully",
        "id": resume.id
    }, status=201)


# ---------------- ANALYZE RESUME ---------------- #

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

    # Detect file type
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in [".doc", ".docx"]:
        text = extract_text_from_docx(file_path)
    else:
        return Response({"error": "Unsupported file format"}, status=400)

    if not text.strip():
        return Response({"error": "Empty resume text"}, status=400)

    # Extract resume skills
    resume_skills = extract_skills(text)

    recommendations = []

    for job in Job.objects.all():

        #  reuse extract_skills
        job_skills = extract_skills(job.job_required_skills)

        # Skip jobs with no detectable skills
        if not job_skills:
            continue

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