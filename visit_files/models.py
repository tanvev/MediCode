from django.db import models

# Create your models here.
from django.db import models
from visits.models import Visit


class VisitFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('xray', 'X-Ray'),
        ('report', 'Report'),
        ('prescription', 'Prescription'),
        ('photo', 'Photo'),
        ('consent', 'Consent Form'),
        ('other', 'Other'),
    )

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='files'
    )

    file = models.FileField(upload_to='visit_files/')
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default='other'
    )

    description = models.CharField(max_length=255, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} - Visit {self.visit.id}"
