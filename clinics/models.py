from django.db import models

# Create your models here.
from django.db import models

class Clinic(models.Model):
    SPECIALTY_CHOICES = (
        ('dental', 'Dental'),
        ('ophthalmology', 'Ophthalmology'),
    )

    name = models.CharField(max_length=255, unique=True)
    specialty = models.CharField(max_length=20, choices=SPECIALTY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.conf import settings


class ClinicMembership(models.Model):
    ROLE_CHOICES = (
        ('frontdesk', 'Front Desk'),
        ('associate', 'Associate Doctor'),
        ('owner', 'Owner Doctor'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'clinic')

    def __str__(self):
        return f"{self.user} - {self.clinic} ({self.role})"
