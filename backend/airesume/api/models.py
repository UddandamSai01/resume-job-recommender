from django.db import models

# Create your models here.

class Resume(models.Model):
    resume=models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"Resume {self.id} Name: {self.resume.name}"
    
class Job(models.Model):
    company_name=models.CharField(max_length=255)
    job_title=models.CharField(max_length=255)
    job_description=models.TextField()
    job_requried_skills=models.TextField()
    job_location=models.CharField(max_length=255)
    job_salary_range=models.CharField(max_length=255)
    job_apply_link=models.URLField(blank=True,null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"