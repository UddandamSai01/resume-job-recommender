from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resume,Job
from .serializers import ResumeSerializer
import os,re
from .utils import extract_text_from_pdf, extract_text_from_docx, extract_skills, match_resume_to_job


# Create your views here.

@api_view(['POST'])
def create_resume(request):
    serializer = ResumeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_resume(request, id):
    resume = Resume.objects.get(id=id)
    serializer = ResumeSerializer(resume)
    return Response(serializer.data)


@api_view(['POST'])
def upload_resume_file(request):
    try:
        if "resume_file" not in request.FILES:
            return Response(
                {"error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        resume = Resume.objects.create(
            resume_file=request.FILES["resume_file"]
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



@api_view(['GET', 'POST'])
def analyze_resume(request, resume_id):
    try:
        # 1️⃣ Check if resume exists
        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2️⃣ Check if file exists
        if not resume.resume_file:
            return Response(
                {"error": "No resume file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_path = resume.resume_file.path

        if not os.path.exists(file_path):
            return Response(
                {"error": "Resume file does not exist on server."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3️⃣ Check file type
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext in [".doc", ".docx"]:
            text = extract_text_from_docx(file_path)
        else:
            return Response(
                {"error": "Unsupported file format. Please upload PDF or DOC/DOCX."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Check if text extraction worked
        if not text or text.strip() == "":
            return Response(
                {"error": "Could not extract text from resume."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5️⃣ Extract skills
        skills = extract_skills(text)

        if not skills:
            return Response(
                {"message": "No skills detected in resume.", "skills": []},
                status=status.HTTP_200_OK
            )

        # 6️⃣ Match with jobs
        def clean_job_skills(text):
            text = text.lower()
            text = re.sub(r"[\/()]", ",", text)
            text = text.replace("and", "")

            skills = [s.strip() for s in text.split(",") if s.strip()]
            return skills
        
        recommendations = []
        for job in Job.objects.all():
            job_skills = clean_job_skills(job.requiredskills)
            score, matched = match_resume_to_job(skills, job_skills)

            recommendations.append({
                "job": job.title,
                "company": job.company,
                "Description":job.description,
                "applyLink": job.applylink,
                "match_score": score,
                "matched_skills": matched,
                "required_skills": job_skills
            })

        # 7️⃣ Final success response
        return Response({
            "extracted_skills": skills,
            "recommendations": recommendations
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # 8️⃣ Catch any unexpected error
        return Response(
            {"error": f"Something went wrong: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )