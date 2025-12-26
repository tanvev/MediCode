from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic


class Lab(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from visits.models import Visit


class LabAssignment(models.Model):
    STATUS_CHOICES = (
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    )

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='lab_assignments'
    )
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    work_description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='assigned'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.lab} - {self.work_description}"
