from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic

class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('staff', 'Staff'),
        ('rent', 'Rent'),
        ('lab', 'Lab'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    expense_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
