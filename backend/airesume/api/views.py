from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os, re

from .models import Resume, Job
from .serializers import ResumeSerializer, JobSerializer
from .utils import extract_text, extract_skills_from_resume, match_resume_to_job


# ---------- BASIC GET APIS ----------

@api_view(['GET'])
def get_resume(request, id):
    try:
        resume = Resume.objects.get(id=id)
    except Resume.DoesNotExist:
        return Response({"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ResumeSerializer(resume)
    return Response(serializer.data)


@api_view(['GET'])
def get_job(request, id):
    try:
        job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = JobSerializer(job)
    return Response(serializer.data)


# ---------- UPLOAD RESUME ----------

@api_view(['POST'])
def upload_resume(request):
    try:
        if "resume" not in request.FILES:
            return Response(
                {"error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        resume = Resume.objects.create(
            resume=request.FILES["resume"]
        )

        return Response(
            {"message": "Resume file uploaded successfully", "id": resume.id},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ---------- ANALYZE RESUME ----------

@api_view(['GET', 'POST'])
def analyze_resume(request, resume_id):
    try:
        # 1️⃣ Check resume exists
        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2️⃣ Check file exists
        if not resume.resume:
            return Response(
                {"error": "No resume file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_path = resume.resume.path

        if not os.path.exists(file_path):
            return Response(
                {"error": "Resume file does not exist on server."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3️⃣ Extract text (clean professional way)
        try:
            text = extract_text(file_path)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Validate extracted text
        if not text or text.strip() == "":
            return Response(
                {"error": "Could not extract text from resume."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5️⃣ Extract skills from resume
        skills = extract_skills_from_resume(text)

        if not skills:
            return Response(
                {"message": "No skills detected in resume.", "skills": []},
                status=status.HTTP_200_OK
            )

        # 6️⃣ Helper to clean job skills text
        def clean_job_skills(text):
            text = text.lower()
            text = re.sub(r"[\/()]", ",", text)
            text = text.replace("and", "")
            skills = [s.strip() for s in text.split(",") if s.strip()]
            return skills

        # 7️⃣ Match resume with all jobs
        recommendations = []

        for job in Job.objects.all():
            job_skills = clean_job_skills(job.job_requried_skills)
            score, matched = match_resume_to_job(skills, job_skills)

            recommendations.append({
                "job": job.job_title,
                "company": job.company_name,
                "description": job.job_description,
                "applyLink": job.job_apply_link,
                "location": job.job_location,
                "salary": job.job_salary_range,
                "required_skills": job_skills,
                "match_score": score,
                "matched_skills": matched,
            })

        # 8️⃣ Final response
        return Response({
            "extracted_skills": skills,
            "recommendations": recommendations
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Something went wrong: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
