from django.contrib import admin
from .models import Resume, Job, Education, Skill
# Register your models here.
admin.site.register(Resume)
admin.site.register(Job)    
admin.site.register(Education)
admin.site.register(Skill)