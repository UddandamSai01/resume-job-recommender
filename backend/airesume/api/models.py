from django.db import models

# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    summary = models.TextField()
    experience = models.TextField()

    def __str__(self):
        return self.name
    
class Education(models.Model):
    resume=models.ForeignKey(Resume, related_name='educations', on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Skill(models.Model):
    resume=models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    requiredskills = models.TextField()

    def __str__(self):
        return self.title