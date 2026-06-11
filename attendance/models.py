from django.db import models
from django.conf import settings

# Create your models here.
class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True,blank=True)
    check_out = models.DateTimeField(null=True,blank=True)
    work_hours = models.DurationField(null=True,blank=True)
    attendance_date =  models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,default="Present")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.attendance_date}"