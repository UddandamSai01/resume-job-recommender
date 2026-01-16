from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import get_resume,get_job,analyze_resume,upload_resume

urlpatterns = [
    path('resume/<int:id>/',get_resume,name='get_resume'),
    path('job/<int:id>/',get_job,name='get_job'),
    path('upload-resume/', upload_resume, name='upload_resume'), 
    path('analyze-resume/<int:resume_id>/', analyze_resume, name='analyze_resume'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
