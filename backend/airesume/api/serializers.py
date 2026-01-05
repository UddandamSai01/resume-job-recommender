from rest_framework import serializers
from .models import Resume, Job, Education, Skill

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['resume','id']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ['resume','id']


class ResumeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = Resume
        fields = [
            'id',
            'name',
            'email',
            'experience',
            'phone',
            'summary',
            'educations',
            'skills',
        ]

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
