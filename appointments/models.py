from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic
from patients.models import Patient
from doctors.models import DoctorProfile


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('checked_in', 'Checked In'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    appointment_time = models.DateTimeField(null=True, blank=True)
    is_walk_in = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_walk_in:
            return f"Walk-in: {self.patient}"
        return f"{self.patient} @ {self.appointment_time}"
