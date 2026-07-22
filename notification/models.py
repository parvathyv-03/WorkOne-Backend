from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Notification(models.Model):
    CATEGORY_CHOICES = (
        ("Leave","Leave"),
        ("Complaint","Complaint"),
        ("HR Announcement","HR Announcement"),
        ("System","System"),
    )

    PRIORITY_CHOICES = (
        ("Low","Low"),
        ("Medium","Medium"),
        ("High","High"),
    )

    STATUS_CHOICES =(
        ("Draft","Draft"),
        ("Published","Published"),
    )

    notification_group = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(max_length=30,choices=CATEGORY_CHOICES)

    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default="Low")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="Published")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title