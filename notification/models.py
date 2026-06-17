from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    CATEGORY_CHOICES = (
        ("Leave","Leave"),
        ("Complaint","Complaint"),
        ("HR Announcement","HR Announcement"),
        ("System","System"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(max_length=30,choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category