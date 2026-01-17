from rest_framework import serializers
from .models import Resume, Job


# ================= RESUME SERIALIZER =================

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "resume_file"]
        read_only_fields = ["id"]


# ================= JOB SERIALIZER =================

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "job_title",
            "company_name",
            "job_location",
            "job_salary",
            "job_description",
            "job_required_skills",
            "job_apply_link",
            "posted_date",
        ]
        read_only_fields = ["id", "posted_date"]
