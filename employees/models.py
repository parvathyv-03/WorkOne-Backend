from django.db import models
from django.conf import settings

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    # basic info
    employee_id = models.CharField(max_length=20,unique=True)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=20)
    marital_status=models.CharField(max_length=20)

    # contact info
    mobile_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15,blank=True)
    current_address = models.TextField()
    permanent_address = models.TextField()

    # employment info
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    employee_type = models.CharField(max_length=50)
    date_of_joining = models.DateField()
    reporting_manager = models.CharField(max_length=100)

    # emergency contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_relationship = models.CharField(max_length=50)
    emergency_contact_number = models.CharField(max_length=15)
    emergency_alternate_number = models.CharField(max_length=15,blank=True)
    profile_image = models.ImageField(upload_to="profiles/",null=True,blank=True)

    def __str__(self):
        return self.employee_id
