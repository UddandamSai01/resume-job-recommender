from django.urls import path
from .views import upload_resume_file, analyze_resume, create_job

urlpatterns = [
    path("upload-resume/", upload_resume_file, name="upload_resume"),
    path("analyze-resume/<int:resume_id>/", analyze_resume, name="analyze_resume"),
    path("create-job/", create_job, name="create_job"),
]
