from django.db import models

# Create your models here.
from django.db import models
from clinics.models import Clinic
import uuid


from django.db import models
from clinics.models import Clinic
import uuid


class Patient(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    # Patient identity
    patient_id = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, db_index=True)

    medical_alerts = models.TextField(blank=True)
    referred_by = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('clinic', 'patient_id')
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['phone']),
            models.Index(fields=['name']),
        ]

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = self.generate_patient_id()
        super().save(*args, **kwargs)

    def generate_patient_id(self):
        """
        Auto-generate clinic-scoped patient ID
        Example: P-12-A4F9C
        """
        return f"P-{self.clinic.id}-{uuid.uuid4().hex[:5].upper()}"

    def __str__(self):
        return f"{self.patient_id} - {self.name}"

class Meta:
    indexes = [
        models.Index(fields=['phone']),
        models.Index(fields=['name']),
        models.Index(fields=['patient_id']),
    ]
