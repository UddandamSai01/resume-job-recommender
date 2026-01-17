from django.db import models

# Create your models here.

class Resume(models.Model):
    resume_file = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"Resume {self.id}"

class Job(models.Model):
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_salary = models.CharField(max_length=100)
    job_description = models.TextField()
    job_required_skills = models.TextField()
    job_location = models.CharField(max_length=255)
    job_apply_link = models.URLField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"