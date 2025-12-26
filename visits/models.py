from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic
from patients.models import Patient
from doctors.models import DoctorProfile
from appointments.models import Appointment


class Visit(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    visit_start = models.DateTimeField(auto_now_add=True)
    visit_end = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit: {self.patient} - {self.visit_start.date()}"
