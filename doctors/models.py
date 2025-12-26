from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from clinics.models import Clinic
from django.core.exceptions import ValidationError


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user} ({self.specialization})"

    def clean(self):
        if self.is_owner:
            exists = DoctorProfile.objects.filter(
                clinic=self.clinic,
                is_owner=True
            ).exclude(pk=self.pk).exists()

            if exists:
                raise ValidationError("Only one owner doctor allowed per clinic.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
class DoctorPayout(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    month = models.DateField()  # use first day of month
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
