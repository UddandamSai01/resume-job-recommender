from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume, Job
from .serializers import ResumeSerializer

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
