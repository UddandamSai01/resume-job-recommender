from django.urls import path
from .views import create_resume, get_resume

urlpatterns = [
    path('resumes/', create_resume, name='create_resume'),
    path('resumes/<int:id>/', get_resume, name='get_resume'),
]