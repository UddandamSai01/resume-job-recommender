from django.db import models

# Create your models here.
class Resume(models.Model):
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    def __str__(self):
        return str(self.id)
    

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    requiredskills = models.TextField()
    applylink = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.title