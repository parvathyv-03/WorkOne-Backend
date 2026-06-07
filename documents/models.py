from django.db import models
from django.conf import settings

# Create your models here.

class EmployeeDocument(models.Model):

    DOCUMENT_TYPES = [
        ("Resume","Resume"),
        ("Degree Certificate","Degree Certificate"),
        ("Experience Certificate","Experience Certificate"),
        ("Offer Letter","Offer Letter"),
    ]

    STATUS_CHOICES = [
        ("Verified","Verified"),
        ("Pending Verification","Pending Verification"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="documents")
    category = models.CharField(max_length=100,choices=DOCUMENT_TYPES)
    document = models.FileField(upload_to="employee_documents/")
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default="Pending Verification")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category
