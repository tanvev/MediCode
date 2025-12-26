from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic


class CommunicationSettings(models.Model):
    clinic = models.OneToOneField(Clinic, on_delete=models.CASCADE)

    send_welcome_message = models.BooleanField(default=True)
    send_appointment_reminders = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comm Settings - {self.clinic.name}"

from patients.models import Patient
from appointments.models import Appointment


class CommunicationLog(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ('welcome', 'Welcome'),
        ('appointment_reminder', 'Appointment Reminder'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    message_type = models.CharField(
        max_length=30,
        choices=MESSAGE_TYPE_CHOICES
    )

    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_type} - {self.patient}"
