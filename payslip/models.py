from django.db import models
from django.conf import settings
# Create your models here.

class Payslip(models.Model):
    STATUS_CHOICES = (
        ("Paid","Paid"),
        ("Pending","Pending")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    month = models.CharField(max_length=20)
    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_earnings = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    pf = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    insurance = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    bonus = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    allowance = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Paid"
    )