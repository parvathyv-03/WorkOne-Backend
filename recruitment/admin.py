from django.contrib import admin
from .models import JobOpening,CandidateApplication

# Register your models here.
admin.site.register(JobOpening)
admin.site.register(CandidateApplication)
