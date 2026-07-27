from django.db import models

# Create your models here.

class JobOpening(models.Model):
    STATUS_CHOICES = [
        ("Open","Open"),
        ("Hiring","Hiring"),
        ("Closed","Closed"),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ("Full Time","Full Time"),
        ("Part Time","Part Time"),
        ("Internship","Internship"),
        ("Contract","Contract"),
        ("Remote","Remote"),
        ("Hybrid","Hybrid"),
    ]

    title = models.CharField(max_length=150)

    department = models.CharField(max_length=100)

    openings = models.PositiveIntegerField(default=1)

    location = models.CharField(max_length=100)

    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES
        )
    
    experience_required = models.CharField(max_length=50)
    
    salary_range = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    description = models.TextField()

    skills = models.TextField(
        help_text="Enter one skill per line",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CandidateApplication(models.Model):

    STATUS_CHOICES =[
        ("Sourced","Sourced"),
        ("In Progress","In Progress"),
        ("Interview","Interview"),
        ("Hired","Hired"),
        ("Rejected","Rejected"),
    ]

    job = models.ForeignKey(
        JobOpening,
        on_delete=models.CASCADE,
        related_name="candidates"
    )

    name = models.CharField(max_length=150)

    email = models.EmailField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Sourced"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name