from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic


class Vendor(models.Model):
    VENDOR_TYPE_CHOICES = (
        ('optical', 'Optical'),
        ('diagnostic', 'Diagnostic'),
        ('surgical', 'Surgical'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPE_CHOICES)
    contact_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.vendor_type})"
from visits.models import Visit


class VendorAssignment(models.Model):
    STATUS_CHOICES = (
        ('assigned', 'Assigned'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='vendor_assignments'
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    purpose = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='assigned'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor} - {self.purpose}"
