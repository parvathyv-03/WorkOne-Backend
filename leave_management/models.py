from django.db import models
from django.conf import settings

# Create your models here.

class LeaveRequest(models.Model):
    LEAVE_TYPES = (
        ("Casual Leave","Casual Leave"),
        ("Sick Leave","Sick Leave"),
        ("Privilege Leave","Privilege Leave"),
    )

    STATUS_CHOICES = (
        ("Pending","Pending"),
        ("Approved","Approved"),
        ("Rejected","Rejected"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    leave_type = models.CharField(
        max_length=30,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_on = models.DateTimeField(
        auto_now_add=True
    )

    def total_days(self):
        return(
            self.end_date -
            self.start_date
        ).days + 1
    
    def __str__(self):
        return f"{self.user.username} - {self.leave_type}"
    
class LeaveBalance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    casual_leave = models.IntegerField(default=10)
    sick_leave = models.IntegerField(default=7)
    privilege_leave = models.IntegerField(default=15)

    def __str__(self):
        return self.user.username