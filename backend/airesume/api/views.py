import os,re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Resume, Job
from .utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_skills,
    match_resume_to_job
)


@api_view(["GET"])
def create_admin(request):
    if User.objects.filter(username="admin").exists():
        return Response({"msg": "Admin already exists"})

    User.objects.create_superuser(
        username="admin",
        password="admin123",
        email="admin@example.com"
    )
    return Response({"msg": "Admin created"})



@api_view(["POST"])
def upload_resume_file(request):
    if "resume_file" not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    resume = Resume.objects.create(resume_file=request.FILES["resume_file"])
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
        job_skills = re.split(r",|/| and ", job.job_required_skills.lower())
        job_skills = [s.strip() for s in job_skills if s.strip()]

        score, matched = match_resume_to_job(resume_skills, job_skills)

        # ✅ FILTER: only 50% and above
        if score >= 50:
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

    # sort best matches first
    recommendations = sorted(
        recommendations,
        key=lambda x: x["match_score"],
        reverse=True
    )

    return Response({
        "extracted_skills": resume_skills,
        "recommendations": recommendations
    })
