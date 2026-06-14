from django.db import models
from django.conf import settings

# Create your models here.
class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ("Workplace","Workplace"),
        ("Technical","Technical"),
        ("Payroll","Payroll"),
        ("Management","Management"),
    )

    STATUS_CHOICES = (
        ("Pending","Pending"),
        ("In Review","In Review"),
        ("Escalated","Escalated"),
        ("Resolved","Resolved"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to="complaints/",blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class ComplaintTimeline(models.Model):
    complaint = models.ForeignKey(Complaint,on_delete=models.CASCADE,related_name="timeline")
    step = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.step
