from django.urls import path
from .views import create_resume, get_resume, upload_resume_file, analyze_resume

urlpatterns = [
    path('resumes/', create_resume, name='create_resume'),
    path('resumes/<int:id>/', get_resume, name='get_resume'),
    path('upload-resume/', upload_resume_file, name='upload_resume_file'),
    path('analyze-resume/<int:resume_id>/', analyze_resume, name='analyze_resume'),
]