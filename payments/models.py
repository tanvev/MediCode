from django.db import models

# Create your models here.
from django.db import models
from visits.models import Visit
from doctors.models import DoctorProfile


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
    )

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    billed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=255, blank=True)

    def balance(self):
        return self.billed_amount - self.paid_amount

    def __str__(self):
        return f"₹{self.paid_amount} - {self.payment_method}"
